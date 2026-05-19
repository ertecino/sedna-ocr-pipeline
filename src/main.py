import os
import shutil
import logging
from pathlib import Path

from src.config import INPUT_DIR, OUTPUT_DIR, ARCHIVE_DIR
from src.extractor import extract_waybill_data
from src.csv_builder import save_to_csv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def process_files():
    logging.info(f"Scanning for files in {INPUT_DIR}")

    # Supported file extensions
    supported_extensions = {".pdf", ".jpg", ".jpeg", ".png"}

    # Make sure output and archive directories exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    INPUT_DIR.mkdir(parents=True, exist_ok=True)

    files_processed = 0

    for file_path in INPUT_DIR.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            logging.info(f"Processing file: {file_path.name}")
            try:
                # 1. Extract Data
                data = extract_waybill_data(str(file_path))
                logging.info(f"Successfully extracted data from {file_path.name}")

                # 2. Build CSV Path
                # Use the document number as filename, fallback to original filename if empty
                csv_filename = f"{data.document_number}.csv" if data.document_number else f"{file_path.stem}.csv"
                # Ensure filename is safe
                csv_filename = "".join(c for c in csv_filename if c.isalnum() or c in (' ', '.', '_', '-')).rstrip()
                if not csv_filename.endswith(".csv"):
                    csv_filename += ".csv"

                output_csv_path = OUTPUT_DIR / csv_filename

                # 3. Save CSV
                save_to_csv(data, output_csv_path)
                logging.info(f"Saved CSV to {output_csv_path}")

                # 4. Move to Archive
                archive_path = ARCHIVE_DIR / file_path.name
                shutil.move(str(file_path), str(archive_path))
                logging.info(f"Moved {file_path.name} to archive")

                files_processed += 1

            except Exception as e:
                logging.error(f"Error processing {file_path.name}: {e}")
                # Optional: Move to an error directory instead of leaving in input

    if files_processed == 0:
        logging.info("No files found to process.")
    else:
        logging.info(f"Finished processing {files_processed} files.")

if __name__ == "__main__":
    process_files()
