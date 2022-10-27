import connexion
from connexion import NoContent
import requests
import yaml
import logging
import logging.config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.background import BackgroundScheduler
from base import Base
from stats import Stats
import datetime
import uuid
from sqlalchemy import func

with open('.\Api project\processing_service/app_conf.yml', 'r') as f:
    app_config = yaml.safe_load(f.read())

with open('.\Api project\processing_service/log_conf.yml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

# DB_ENGINE = create_engine(f'mysql+pymysql://{app_config["datastore"]["user"]}:{app_config["datastore"]["password"]}@{app_config["datastore"]["hostname"]}:{app_config["datastore"]["port"]}/{app_config["datastore"]["db"]}')
# Base.metadata.bind = DB_ENGINE
# DB_SESSION = sessionmaker(bind=DB_ENGINE)

DB_ENGINE = create_engine("sqlite:///%s" %app_config["datastore"]["filename"])
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(  populate_stats,
                    'interval',
                    seconds=app_config['scheduler']['period_sec'])
    sched.start()

# def get_stats(body):
#     """ Receives a auction post reading """
#     trace = body['traceId']
#     logging.debug("Received event postAuction request with a trace id of " + trace)

#     session = DB_SESSION()
#     listeditem =    postAuctionClass(body['itemID'],
#                 body['traceId'],
#                 body['sellerID'],
#                 body['closingTime'],
#                 body['maxCount'],
#                 body['minPrice'],
#                 body['instaBuyPrice'],
#                 body['description'])

#     session.add(listeditem)

#     session.commit()
#     session.close()
#     logger.debug('Received postAuction event (Id: ' + trace + ')')


#     return NoContent, 201



# def get_stats(timestamp):
#     """ Gets bids after the timestamp """
#     session = DB_SESSION()
#     timestamp_datetime = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
#     readings = session.query(bidAuctionClass).filter(bidAuctionClass.date_created >= timestamp_datetime)
#     results = session.query(Stats).order_by(Stats.last_updated.desc())
#     results_list = []
#     for reading in readings:
#         results_list.append(reading.to_dict())
#     session.close()

#     logger.info("Query for new bids after %s returns %d results" %
#         (timestamp, len(results_list)))
#     return results_list, 200

def populate_stats():
    trace = str(uuid.uuid4())
    # periodically update stats
    curr_time = datetime.datetime.now()

    logger.info(f'Periodic processing has started  with traceID {trace}...')

    session = DB_SESSION()
    check =  session.query(Stats).order_by(Stats.last_updated.desc()).first()


    default_time = '1900-10-15T16:47:03Z'
    if (check == None ):
        latestime = default_time
    else: 
        results = session.query(Stats).order_by(Stats.last_updated.desc())[0].to_dict()
        latestime = (results["last_updated"]).strftime("%Y-%m-%dT%H:%M:%SZ")
    # latestime = default_time

    get_bids = requests.get(app_config["scheduler"]["getBids"]["url"] + '?timestamp=' + latestime, headers={
    'Content-Type': 'application/json'})

    get_bids__status_code = get_bids.status_code
    get_bids__json = get_bids.json()
    print("get_bids", get_bids__json, "\n-----------------\n")
    print(len(get_bids__json))

    get_items = requests.get(app_config["scheduler"]["getItems"]["url"] + '?timestamp=' + latestime, headers={
    'Content-Type': 'application/json'})
    
    get_items__status_code = get_items.status_code
    get_items__json = get_items.json()
    print("get_items", get_items__json)
    print(len(get_items__json))

    if get_bids__status_code== 200:
        logger.info(f"Received {len(get_bids__json)} events.")
    else:
        logger.error(f"The storage API has returned code {get_bids.status_code}.")

    if get_items__status_code == 200:
        logger.info(f"Received {len(get_items__json)} events.")
    else:
        logger.error(f"The storage API has returned code {get_items.status_code}.")

    if (len(get_bids__json) != 0) :
        num_bids = int(len(get_bids__json))
        max_bid = max(get_bids__json, key=lambda x:x['bidPrice'])['bidPrice']
        for x in get_bids__json:
            logger.debug(f'events have the trace ids of { x["traceId"] }')
    else: 
        num_bids = 0
        max_bid = 0
    if ((len(get_items__json)) != 0):
        num_items_listed = int(len(get_items__json))
        max_instabuy_price = max(get_items__json, key=lambda x:x['instaBuyPrice'])['instaBuyPrice']
        for x in get_items__json:
            logger.debug(f'events have the trace ids of { x["traceId"] }')
    else:
        num_items_listed = 0
        max_instabuy_price = 0
    last_updated = curr_time
    traceID = trace
    rows = session.query(func.count(Stats.id)).scalar()

    if rows > 0:
        if not results:
            results = session.query(Stats).order_by(Stats.last_updated.desc())[0].to_dict()
        results
        num_bids += int(results["num_bids"])
        max_bid += int(results["max_bid"])
        num_items_listed += int(results["num_items_listed"])
        max_instabuy_price += int(results["max_instabuy_price"])

    stats = Stats(num_bids,
                max_bid,
                num_items_listed,
                max_instabuy_price,
                last_updated,
                traceID) 

    session.add(stats)
    session.commit()
    session.close()




def get_stats():
    #Gets new blood pressure readings after the timestamp 
   
    logger.info("Received request for getting the latest stats, processing...")
    session = DB_SESSION()
    check =  session.query(Stats).order_by(Stats.last_updated.desc()).first()

    if (check == None ):
        return "“Statistics do not exist”", 404
    else:
        results = session.query(Stats).order_by(Stats.last_updated.desc())
        session.close()
        print(results)

        result = results[0].to_dict()

        logger.debug(f"The latest stats:\n{result}\n")
        logger.info("The request has been completed.")

    return result, 200



app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)
logger = logging.getLogger('basicLogger')

if __name__ == "__main__":
# run our standalone gevent server
    init_scheduler()
    app.run(port=8100, use_reloader=False)
