import connexion
from connexion import NoContent
import yaml
import logging
import logging.config
from sqlalchemy import create_engine 
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from base import Base
from post_Auction import postAuctionClass
from bid_Auction import bidAuctionClass
import datetime
import json
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread 
from os import environ

with open('./app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('./log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

DB_ENGINE = create_engine(f'mysql+pymysql://{app_config["datastore"]["user"]}:{app_config["datastore"]["password"]}@{environ["KAFKA_DNS"]}:{app_config["datastore"]["port"]}/{app_config["datastore"]["db"]}')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def postAuction(body):
    """ Receives a auction post reading """
    trace = body['traceId']
    logging.info(f'connecting to DB. Hostname:{environ["KAFKA_DNS"]} on port: {app_config["datastore"]["port"]}')
    logging.debug("Received event postAuction request with a trace id of " + trace)

    session = DB_SESSION()
    listeditem =    postAuctionClass(body['itemID'],
                body['traceId'],
                body['sellerID'],
                body['closingTime'],
                body['maxCount'],
                body['minPrice'],
                body['instaBuyPrice'],
                body['description'])

    session.add(listeditem)

    session.commit()
    session.close()
    logger.debug('Received postAuction event (Id: ' + trace + ')')
    logger.info(f'connecting to DB. Hostname:{environ["KAFKA_DNS"]} on port: {app_config["datastore"]["port"]}')


    return NoContent, 201


def bidAuction(body):
    """ Receives a bids """

    session = DB_SESSION()
    trace = body['traceId']
    logging.debug("Received event bidAuction request with a trace id of " + trace)
    logging.info(f'connecting to DB. Hostname:{environ["KAFKA_DNS"]} on port: {app_config["datastore"]["port"]}')

    bid = bidAuctionClass(body['traceId'],
                   body['itemID'],
                   body['bidderID'],
                   body['bidID'],
                   body['bidCount'],
                   body['bidPrice'],
                   body['bidTime'])

    session.add(bid)

    session.commit()
    session.close()
    logger.info(f'connecting to DB. Hostname:{environ["KAFKA_DNS"]} on port: {app_config["datastore"]["port"]}')

    logger.debug('Received bidAuction event (Id: ' + trace + ')')

    return NoContent, 201

def get_new_bids(timestamp, end_timestamp):
    """ Gets bids after the timestamp """
    session = DB_SESSION()
    if (timestamp == "None"):
        timestamp_datetime = "2002-10-15T16:47:03Z"
    else:
        timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    if (end_timestamp == "None"):
        now = datetime.now()
        end_timestamp_datetime = now.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%S")

    readings = session.query(bidAuctionClass).filter(
        and_ (bidAuctionClass.date_created >= timestamp_datetime,
        bidAuctionClass.date_created < end_timestamp_datetime))

    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()

    logger.info("Query for new bids after %s returns %d results" %
        (timestamp, len(results_list)))
    return results_list, 200


def get_new_items(timestamp, end_timestamp):
    """ Gets new item  readings the timestamp """
    session = DB_SESSION()
    if (timestamp == "None"):
        timestamp_datetime = "2002-10-15T16:47:03Z"
    else:
        timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    if (end_timestamp == "None"):
        now = datetime.now()
        end_timestamp_datetime = now.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%dT%H:%M:%S")

    readings = session.query(postAuctionClass).filter(
        and_ (postAuctionClass.date_created >= timestamp_datetime,
postAuctionClass.date_created < end_timestamp_datetime))

    

    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    
    logger.info("Query for new item postings after %s returns %d results" %
        (timestamp, len(results_list)))
    return results_list, 200

def process_messages():
    """ Process event messages """
    # logger.debug(f'{app_config}')
    hostname = f'{environ["KAFKA_DNS"]}:{app_config["events"]["port"]}'

    # logger.info(f"attempting to connect to {hostname}")
    # tries = 0
    # while ((tries < app_config['datastore']['retries']) and ()):
    #     tries += 1
    curr_retry = 0
    while curr_retry < app_config["events"]["max_retry"]:
        try:
            logger.info(f"Trying to connect to Kafka, retry count: {curr_retry}")
            client = KafkaClient(hosts=hostname)
            topic = client.topics[str.encode(app_config["events"]["topic"])]
        except:
            logger.error("Connection Failed!")
            time.sleep(app_config["events"]["sleep"])
        curr_retry += 1
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                        reset_offset_on_start=False,
                                        auto_offset_reset=OffsetType.LATEST)
    # This is blocking - it will wait for a new message
    # client = KafkaClient(hosts=hostname)
    # topic = client.topics[str.encode(app_config["events"]["topic"])]
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                            reset_offset_on_start=False,
                                            auto_offset_reset=OffsetType.LATEST)
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "postAuction": # Change this to your event type
            postAuction(payload)
            logger.info(f'posting {msg} storage')
        elif msg["type"] == "bidAuction": # Change this to your event type
            bidAuction(payload)
            logger.info(f'posting {msg} storage')
        consumer.commit_offsets()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)
logger = logging.getLogger('basicLogger')

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
    
