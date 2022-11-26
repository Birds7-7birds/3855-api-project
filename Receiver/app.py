import os
import logging
import logging.config
import yaml
import uuid
import json
import datetime
import time
import connexion
from connexion import NoContent
import swagger_ui_bundle
from pykafka import KafkaClient


def healthcheck():
    return 200

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"
with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())

# External Logging Configuration
with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    logger = logging.getLogger('basicLogger')

logger.info(f"App Conf File: {app_conf_file}")
logger.info(f"Log Conf File: {log_conf_file}")

# with open('./app_conf.yml', 'r') as f:
#     app_config = yaml.safe_load(f.read())
# with open('./log_conf.yml', 'r') as f:
#     log_config = yaml.safe_load(f.read())
#     logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

CURR_RETRY = 0
while CURR_RETRY < app_config["events"]["max_retry"]:
    CURR_RETRY += 1
    try:
        logger.info(f"Trying to connect to Kafka, retry count: {CURR_RETRY}")
        client = KafkaClient(hosts=f'{os.environ["KAFKA_DNS"]}:{app_config["events"]["port"]}')
        topic = client.topics[str.encode(app_config["events"]["topic"])]
        producer = topic.get_sync_producer()
    except:
        logger.error("Connection Failed!")
        time.sleep(app_config["events"]["sleep"])


def post_auction(body):
    trace = str(uuid.uuid4())
    body["traceId"] = trace
    logging.info("Received event postAuction request with a trace id of " + trace)

    msg = { "type": "postAuction",
            "datetime" :
                datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S"),
            "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logger.info('Returned postAuction event response(Id: ' + trace + ') with status 201 i hope')

    return "done  👍 ", 201

def bid_auction(body):
    trace = str(uuid.uuid4())
    body["traceId"] = trace
    logging.info("Received event bidAuction request with a trace id of " + trace)

    msg = { "type": "bidAuction",
            "datetime" :
                datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S"),
            "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    # logger.info('Returned postAuction event response(Id: ' + trace + ') with status ' + str(x.status_code))
    logger.info('Returned bidAuction event response(Id: ' + trace + ') with status 201 i hope')

    return "done  👍", 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", base_path="/receiver", strict_validation=True, validate_responses=True)
if __name__ == "__main__":

    app.run(port=8080)
