from .logging_config import setup_logging, get_logger

# Set up default logging configuration
setup_logging()

# Create a logger for the package
logger = get_logger(__name__)

# def main() -> None:
#     print("Hello from zp-velodata!")