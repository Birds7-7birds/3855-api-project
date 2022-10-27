from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class bidAuctionClass(Base):
    """ bid on item """

    __tablename__ = "bid_Auction"

    traceId = Column(String(250), nullable=True)
    id = Column(Integer, primary_key=True)
    itemID = Column(String(250), nullable=False)
    bidderID = Column(String(250), nullable=False)
    bidID = Column(String(250), nullable=False)
    bidTime = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    bidCount = Column(Integer, nullable=False)
    bidPrice = Column(Integer, nullable=False)

    def __init__(self, traceId, itemID, bidderID, bidID, bidCount, bidPrice, bidTime):
        """ Initializes a bid """
        self.traceId = traceId
        self.itemID = itemID
        self.bidderID = bidderID
        self.bidID = bidID
        self.bidTime = bidTime
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.bidCount = bidCount
        self.bidPrice = bidPrice

        

    def to_dict(self):
        """ Dictionary Representation of a bid """
        dict = {}
        dict['id'] = self.id
        dict['traceId'] = self.traceId
        dict['itemID'] = self.itemID
        dict['bidderID'] = self.bidderID
        dict['bidID'] = self.bidID
        dict['bidCount'] = self.bidCount
        dict['bidPrice'] = self.bidPrice
        dict['bidTime'] = self.bidTime
        dict['date_created'] = self.date_created

        return dict
