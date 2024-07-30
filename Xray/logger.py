
import logging
import os
from datetime import datetime

# Ensure the log directory path is correctly formatted
log_directory = "D:\\DeepLearning\\logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Generate a log file name with the current date and time
log_filename = datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".log"

# Combine the directory and file name to form the full path
logs_path = os.path.join(log_directory, log_filename)

# Now create the log file directory if it doesn't exist
os.makedirs(log_directory, exist_ok=True)

# Log setup code...
logging.basicConfig(
    filename=log_filename,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)