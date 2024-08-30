import logging

# Basic logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

logging.debug("Debug message: This should appear in the console.")
logging.info("Info message: Logging is working.")
logging.warning("Warning message: There might be issues if this doesn't show.")
logging.error("Error message: Check your setup.")
logging.critical("Critical message: Logging setup complete.")
