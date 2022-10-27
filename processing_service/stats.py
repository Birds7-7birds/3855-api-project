from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class Stats(Base):
    """ post auction """

    __tablename__ = "stats"

    id = Column(Integer, primary_key=True)
    num_bids = Column(Integer, nullable=False)
    max_bid = Column(Integer, nullable=False)
    num_items_listed = Column(Integer, nullable=False)
    max_instabuy_price = Column(Integer, nullable=False)
    last_updated = Column(DateTime, nullable=False)
    traceID = Column(String(), nullable=False)


    def __init__(self, num_bids, max_bid, num_items_listed, max_instabuy_price, last_updated, traceID):
        """ Initializes a item post  """
        self.num_items_listed = num_items_listed
        self.num_bids = num_bids
        self.max_bid = max_bid
        self.max_instabuy_price = max_instabuy_price
        self.last_updated = last_updated 
        self.traceID = traceID

    def to_dict(self):
        """ Dictionary Representation of a item posting """
        dict = {}
        dict['id'] = self.id
        dict['num_items_listed'] = self.num_items_listed
        dict['max_bid'] = self.max_bid
        dict['max_instabuy_price'] = self.max_instabuy_price
        dict['num_bids'] = self.num_bids
        dict['last_updated'] = self.last_updated
        dict['traceID'] = self.traceID


        return dict
