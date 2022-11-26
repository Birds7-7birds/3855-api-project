import connexion
from connexion import NoContent
import requests
import yaml
import logging
import logging.config
from apscheduler.schedulers.background import BackgroundScheduler
from os import environ
import os
import datetime 
import json

with open('./app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('./log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(  check_health,
                    'interval',
                    seconds=app_config['scheduler']['period_sec'])
    sched.start()

EVENT_FILE = app_config["files"]["event_file"]
MAX_EVENTS=app_config["files"]["max_events"]

data = []

if (not (os.path.isfile(EVENT_FILE))):
    with open(EVENT_FILE, mode='a'): pass

def get_stats():
    with open(EVENT_FILE,"r") as f:
        data = json.load(f)
    if (data == None ):
        return "“i dont got what ya want exist”", 404
    else:
        logger.info(data[0])
        result = data[0]

        logger.debug(f"The latest stats:\n{result}\n")
        logger.info("The request has been completed.")

    return result, 200

def check_health():
    curr_time = datetime.datetime.now()
    curr_time_str = curr_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    health = {}

    receiver_health = app_config["receiverHealth"]
    storage_health = app_config["storageHealth"]
    processing_health = app_config["processingHealth"]
    audit_health = app_config["auditHealth"]
    timeout = app_config["timeout"]

    health_list = [receiver_health, storage_health, processing_health, audit_health]

    for health_check in health_list:
        try:
# requests.get("http://" + environ["KAFKA_DNS"] +"/receiver" +"/healthcheck", timeout=app_config['scheduler']['timeout'])
            requests.get("http://" + environ["KAFKA_DNS"] + health_check["url"], timeout=timeout)
            health[health_check["service"]] = "Running"
        except Exception as e:
            health[health_check["service"]] = "Down"

    health["last_updated"] = curr_time_str

    logger.info(f"Health Check: {health}")
    dict_in_a_list = [health]
    with open(EVENT_FILE, "w") as f:
        json.dump(dict_in_a_list, f, indent=4)

    return health, 200


app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", base_path="/healthcheck",strict_validation=True, validate_responses=True)
logger = logging.getLogger('basicLogger')


if __name__ == "__main__":
# run our standalone gevent server
    init_scheduler()
    app.run(port=8120, use_reloader=False)
