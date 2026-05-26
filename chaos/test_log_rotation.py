import os
import logging
from logging.handlers import RotatingFileHandler

def setup_test_logger(log_file, max_bytes, backup_count):
    # Remove old log files if present
    for i in range(backup_count + 1):
        try:
            os.remove(f"{log_file}.{i}")
        except FileNotFoundError:
            pass
    try:
        os.remove(log_file)
    except FileNotFoundError:
        pass

    logger = logging.getLogger("test_rotation")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    logger.handlers = [handler]
    return logger

def test_log_rotation():
    log_file = "test_rotation.log"
    max_bytes = 64  # Even smaller for ultra-fast rotation
    backup_count = 2

    logger = setup_test_logger(log_file, max_bytes, backup_count)

    print("Starting log writes...")
    # Write very few log entries to trigger rotation quickly
    for i in range(4):
        logger.info(f"Test log entry {i} - {'x'*10}")
    print("Finished log writes.")

    # Check that rotated log files exist
    rotated_files = [f"{log_file}.{i}" for i in range(1, backup_count+1)]
    found = [os.path.exists(f) for f in rotated_files]
    print("Rotated file existence:", list(zip(rotated_files, found)))
    assert all(found), f"Not all rotated log files found: {rotated_files}"
    print("Log rotation test passed. Rotated files:", rotated_files)

if __name__ == "__main__":
    test_log_rotation()
