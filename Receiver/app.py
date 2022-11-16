import swagger_ui_bundle
import connexion
import os
import logging
import logging.config
import yaml
import uuid
import json
from pykafka import KafkaClient
import datetime
from connexion import NoContent
import requests
import time
from os import environ

with open('./app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())
with open('./log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

# curr_retry = 0
# while curr_retry < app_config["events"]["max_retry"]:
#     try:
#         logger.info(f"Trying to connect to Kafka, retry count: {curr_retry}")
#         client = KafkaClient(hosts=hostname)
#         topic = client.topics[str.encode(app_config["events"]["topic"])]
#         producer = topic.get_sync_producer()
#     except:
#         logger.error("Connection Failed!")
#         time.sleep(app_config["events"]["sleep"])

def postAuction(body):
    trace = str(uuid.uuid4())
    body["traceId"] = trace
    logging.info("Received event postAuction request with a trace id of " + trace)
    curr_retry = 0
    while curr_retry < app_config["events"]["max_retry"]:
        try:
            logger.info(f"Trying to connect to Kafka, retry count: {curr_retry}")
            client = KafkaClient(hosts=f'{environ["KAFKA_DNS"]}:{app_config["events"]["port"]}')
            topic = client.topics[str.encode(app_config["events"]["topic"])]
            producer = topic.get_sync_producer()
        except:
            logger.error("Connection Failed!")
            time.sleep(app_config["events"]["sleep"])

    msg = { "type": "postAuction",
            "datetime" :
                datetime.datetime.now().strftime(
                    "%Y-%m-%dT%H:%M:%S"),
            "payload": body }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    # logger.info('Returned postAuction event response(Id: ' + trace + ') with status ' + str(x.status_code))
    logger.info('Returned postAuction event response(Id: ' + trace + ') with status 201 i hope')

    return "done  👍 ", 201

def bidAuction(body):
    trace = str(uuid.uuid4())
    body["traceId"] = trace
    logging.info("Received event bidAuction request with a trace id of " + trace)


    curr_retry = 0
    while curr_retry < app_config["events"]["max_retry"]:
        try:
            logger.info(f"Trying to connect to Kafka, retry count: {curr_retry}")
            client = KafkaClient(hosts=f'{environ["KAFKA_DNS"]}:{app_config["events"]["port"]}')
            topic = client.topics[str.encode(app_config["events"]["topic"])]
            producer = topic.get_sync_producer()
        except:
            logger.error("Connection Failed!")
            time.sleep(app_config["events"]["sleep"])

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
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)
logger = logging.getLogger('basicLogger')

if __name__ == "__main__":

    app.run(port=8080)