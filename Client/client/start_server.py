import uvicorn
from config.load_settings import (APP_HOST, APP_PORT, WORKERS, LOGS_PATH)
from src.utils.utils import check_dir
import time

if __name__ == "__main__":
    check_dir(LOGS_PATH)
    while True:
        try:
            uvicorn.run("server:app", host=APP_HOST, port=int(APP_PORT), workers=int(WORKERS), log_config="config/logconfig.ini") #add absolute path to log_config if you want to try in local
        except:
            time.sleep(5)
        else:
            break;   
