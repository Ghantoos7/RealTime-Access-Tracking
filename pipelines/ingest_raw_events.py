import pandas as pd
from utils import RAW_EXCEL_PATH, TOPIC_RAW_EVENTS, CHOSEN_COLUMNS
from utils import create_producer, get_logger, get_mongo_collection



mongo_col = get_mongo_collection("raw_events")
logger = get_logger("[INGESTION]", "rfid_stream.log")

def load_sorted_rows_from_excel(path, iterations=10):
    """
    Loads and returns sorted RFID rows from all sheets in the Excel file across multiple passes.
    """
    logger.info(f"READ - path={path}")

    xls = pd.ExcelFile(path)
    all_rows = []

    for i in range(iterations):
        for sheet in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet)
            df.columns = [col.strip().lower().replace(" ", "") for col in df.columns]
            df = df[[col for col in CHOSEN_COLUMNS if col in df.columns]]
            df['sheet'] = sheet
            df = df.dropna(subset=['epc', 'tagtime', 'baselogicaldevice'])
            all_rows.append(df)
            logger.debug(f"PARSED - sheet={sheet} rows={len(df)}.")

    df = pd.concat(all_rows, ignore_index=True)
    df['tagtime'] = pd.to_numeric(df['tagtime'], errors='coerce')
    df = df.dropna(subset=['tagtime'])

    logger.info(f"PARSED - total_rows={len(df)}")

    return df.sort_values(by='tagtime')

def start_raw_pipeline():
    """
    Streams cleaned and sorted RFID raw events from Excel to Kafka in chronological order.
    """
    logger.info("STARTED - pipeline=excel_to_kafka")

    df = load_sorted_rows_from_excel(RAW_EXCEL_PATH)
    total_sent = 0
    producer = create_producer()
    
    for idx, row in df.iterrows():
        event = row.to_dict()
        try:
            event['rssi'] = float(event.get('rssi', -999))
            event['tagtime'] = int(event['tagtime'])
            producer.send(TOPIC_RAW_EVENTS, value=event)
            mongo_col.insert_one(event)
            logger.debug(f"SENT - epc={event.get('epc')} tagtime={event['tagtime']} rssi={event['rssi']}")
            total_sent += 1
        except Exception as e:
            logger.warning(f"SKIPPED - row={idx} reason={e} epc={event.get('epc')}")

    producer.flush()
    logger.info(f"COMPLETED - total_sent={total_sent}")

if __name__ == "__main__":
    start_raw_pipeline()
