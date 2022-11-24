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


EVENT_FILE = "health.json"
MAX_EVENTS=1

data = []

if (not (os.path.isfile(EVENT_FILE))):
    with open(EVENT_FILE, mode='a'): pass


def make_json_keep_10(post_info):
    data.insert(0, post_info)
    while len(data) > MAX_EVENTS:
        data.pop()
    with open(EVENT_FILE,"w") as f:
        f.write(json.dumps(data, indent=4))


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
    # receiver_health = requests.get(app_config["eventstore"]["url"] + app_config["scheduler"]["getBids"]["url"] + '?timestamp=' + latestime, headers={


def check_health():
    #Gets new blood pressure readings after the timestamp 
    receiver = requests.get("http://" + environ["KAFKA_DNS"] +"/receiver" +app_config['scheduler']['health']['url'], timeout=app_config['scheduler']['timeout'])
    audit = requests.get("http://" +environ["KAFKA_DNS"]+"/audit_log" + app_config['scheduler']['health']['url'], timeout=app_config['scheduler']['timeout'])
    processing_service = requests.get("http://" +environ["KAFKA_DNS"] +"/processing" + app_config['scheduler']['health']['url'], timeout=app_config['scheduler']['timeout'])
    storage = requests.get("http://" +environ["KAFKA_DNS"] +"/storage" + app_config['scheduler']['health']['url'], timeout=app_config['scheduler']['timeout'])

    logger.info(f"receiver returned {receiver.status_code}.")
    logger.info(f"audit returned {audit.status_code}.")
    logger.info(f"processing_service returned {processing_service.status_code}.")
    logger.info(f"storage returned {storage.status_code}.")
    current_datetime = datetime.datetime.now()
    last_updated = current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
    if receiver.status_code != 200:
        receiver.status_code = "Down"
    else:
        receiver.status_code = "Running"
    if audit.status_code != 200:
        audit.status_code = "Down"
    else:
        audit.status_code = "Running"
    if processing_service.status_code != 200:
        processing_service.status_code = "Down"
    else:
        processing_service.status_code = "Running"
    if storage.status_code != 200:
        storage.status_code = "Down"
    else:
        storage.status_code = "Running"
    item_info = {
        "last_updated": last_updated,
        "receiver": receiver.status_code,
        "audit": audit.status_code,
        "processing": processing_service.status_code,
        "storage": storage.status_code,
        # }
        
    }

    make_json_keep_10(item_info)
    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", base_path="/healthcheck",strict_validation=True, validate_responses=True)
logger = logging.getLogger('basicLogger')


if __name__ == "__main__":
# run our standalone gevent server
    init_scheduler()
    app.run(port=8120, use_reloader=False)
