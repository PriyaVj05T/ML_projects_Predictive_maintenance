

import os
import logging
from datetime import datetime
from importlib import reload

reload(logging)

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_path=os.path.join(os.getcwd(),"logs")
os.makedirs(log_path,exist_ok=True)
LOG_FILEPATH=os.path.join(log_path,LOG_FILE)

#LOGGING CONFIGURATION
logging.basicConfig(level=logging.INFO,
                    filename=LOG_FILEPATH,
                    format="[%(asctime)s] %(lineno)d %(name)s -%(levelname)s -%(message)s"
                    )

# Optional: also log to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] %(lineno)d %(name)s -%(levelname)s -%(message)s")
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)
