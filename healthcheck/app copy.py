import swagger_ui_bundle
import connexion
import json
import datetime
import os
from connexion import NoContent

EVENT_FILE = "events.json"
MAX_EVENTS=10

data = []

if (not (os.path.isfile(EVENT_FILE))):
    with open(EVENT_FILE, mode='a'): pass


def make_body_list_and_add_time(post_info):
    data.insert(0, post_info)
    while len(data) > MAX_EVENTS:
        data.pop()
    with open(EVENT_FILE,"w") as f:
        f.write(json.dumps(data, indent=4))
    # file_handle = open(EVENT_FILE,"w")
    # file_handle.write(json.dumps(data, indent=4))
    # file_handle.close()

# def log_contents(content):
#     file_handle = open(EVENT_FILE,"a")
#     file_handle.write(content)
#     file_handle.close()

def postAuction(body):
    current_datetime = datetime.datetime.now()
    current_datetime_str = current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
    item_info = {
        "received_timestamp": current_datetime_str,
        "item_description": body["itemID"] + " is created by " + body["sellerID"],
        # "item_info":{
        #     "description": body["description"],
        #     "sellerID": body["sellerID"],
        #     "minPrice": body["minPrice"],
        # }
        
    }
    make_body_list_and_add_time(item_info)
    return NoContent, 201

def bidAuction(body):
    current_datetime = datetime.datetime.now()
    current_datetime_str = current_datetime.strftime("%Y-%m-%dT%H:%M:%SZ")
    bid_info = {
        "received_timestamp": current_datetime_str,
        "bid_description": body["bidID"] + " bid on " + body["itemID"] + "for " + str(body["bidPrice"]) + "each",
        # "bid_info": {
        #     "item_ID":body["itemID"],
        #     "bidder_id":body["bidderID"],
        #     "bid_Price": body["bidPrice"],
        # },
    }
    make_body_list_and_add_time(bid_info)
    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yml", strict_validation=True, validate_responses=True)
if __name__ == "__main__":
    app.run(port=8080)