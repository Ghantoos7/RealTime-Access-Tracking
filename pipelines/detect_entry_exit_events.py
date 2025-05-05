from collections import defaultdict, deque
from utils import TOPIC_DETECTED_EVENTS, GROUP_DETECTOR, MAX_HISTORY, COOLDOWN_MS, RSSI_THRESHOLD
from utils import create_producer, create_consumer, get_logger, get_mongo_collection
from utils import time_score_by_direction, rssi_score_by_direction, count_score, trend_score



mongo_col = get_mongo_collection("detected_events")
logger = get_logger("[DETECTOR]", "rfid_stream.log")

def detect_event(history):
    """
    Detects whether an entry or exit event occurred based on scoring logic.
    """
    
    if len(history) < MAX_HISTORY:
        return None

    current_direction = history[-1]['direction']
    current_time = history[-1]['tagtime']

    scores = {
        "time": time_score_by_direction(history, current_time),
        "rssi": rssi_score_by_direction(history),
        "count": count_score([e['direction'] for e in history]),
        "trend": trend_score(history)
    }

    in_total = sum(scores[metric]["In"] for metric in scores)
    out_total = sum(scores[metric]["Out"] for metric in scores)

    if abs(scores["rssi"]["In"] - scores["rssi"]["Out"]) > 10:
        return "entry" if scores["rssi"]["In"] > scores["rssi"]["Out"] else "exit"

    if all(e["direction"] == current_direction for e in history):
        if current_direction == "In" and (in_total - out_total) > 5:
            return "entry"
        if current_direction == "Out" and (out_total - in_total) > 5:
            return "exit"
        return None

    if abs(in_total - out_total) < 2:
        return None
    return "entry" if in_total > out_total else "exit"

def start_detection_pipeline():
    """
    Consumes cleaned RFID events, applies detection logic, and publishes entry/exit events.
    """
    logger.info("STARTED - action=entry_exit_detection")

    producer = create_producer()
    consumer = create_consumer('rfid-clean-events', group_id=GROUP_DETECTOR, auto_offset_reset='latest')

    tag_states = defaultdict(lambda: {
        "history": deque(maxlen=MAX_HISTORY),
        "inside": False,
        "last_event": None,
        "last_decision_time": None
    })

    logger.info("LISTENING - topic=rfid-clean-events")

    for msg in consumer:
        data = msg.value
        epc = data.get('epc')
        rssi = data.get('rssi')
        direction = data.get('direction')
        tagtime = data.get('tagtime')
        timestamp = data.get('timestamp')
        door = data.get('door')
        box = data.get('box')

        if None in [epc, rssi, direction, tagtime, timestamp]:
            logger.warning(f"SKIPPED - reason=missing_fields epc={epc} data={data}")
            continue

        state = tag_states[epc]
        state['history'].append({
            "rssi": rssi,
            "direction": direction,
            "tagtime": tagtime,
            "timestamp": timestamp
        })

        last_time = state.get("last_decision_time")
        if last_time is not None:
            time_diff = tagtime - last_time
            if time_diff < COOLDOWN_MS and rssi < RSSI_THRESHOLD:
                logger.debug(f"SUPPRESSED - epc={epc} time_diff={time_diff} rssi={rssi}")
                continue

        result = detect_event(state['history'])
        if result == state["last_event"]:
            logger.debug(f"NO_CHANGE - epc={epc} event={result}")
            continue
        state["last_event"] = result

        if (result == "entry" and direction != "In") or (result == "exit" and direction != "Out"):
            logger.debug(f"MISMATCH - epc={epc} result={result} raw_direction={direction}")
            continue

        if result == "entry" and not state['inside']:
            state['inside'] = True
            state['last_decision_time'] = tagtime
            producer.send(TOPIC_DETECTED_EVENTS, {**data, "event": "entry"})
            mongo_col.insert_one({**data, "event": result})
            logger.info(f"DETECTED - epc={epc} event=entry door={door} box={box} rssi={rssi} time={timestamp}")

        elif result == "exit" and state['inside']:
            state['inside'] = False
            state['last_decision_time'] = tagtime
            producer.send(TOPIC_DETECTED_EVENTS, {**data, "event": "exit"})
            mongo_col.insert_one({**data, "event": result})
            logger.info(f"DETECTED - epc={epc} event=exit door={door} box={box} rssi={rssi} time={timestamp}")

    producer.flush()
    logger.info("COMPLETED - action=entry_exit_flush")

if __name__ == "__main__":
    start_detection_pipeline()
