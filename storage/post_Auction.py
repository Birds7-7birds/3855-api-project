from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class postAuctionClass(Base):
    """ post auction """

    __tablename__ = "post_Auction"

    traceId = Column(String(250), nullable=True)
    id = Column(Integer, primary_key=True)
    itemID = Column(String(250), nullable=False)
    sellerID = Column(String(250), nullable=False)
    closingTime = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    maxCount = Column(Integer, nullable=False)
    minPrice = Column(Integer, nullable=False)
    instaBuyPrice = Column(Integer, nullable=False)
    description = Column(String(250), nullable=False)

    def __init__(self, itemID, traceId, sellerID, closingTime, maxCount, minPrice, instaBuyPrice, description):
        """ Initializes a item post  """
        self.traceId = traceId
        self.itemID = itemID
        self.sellerID = sellerID
        self.closingTime = closingTime
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
        self.maxCount = maxCount
        self.minPrice = minPrice
        self.instaBuyPrice = instaBuyPrice
        self.description = description

    def to_dict(self):
        """ Dictionary Representation of a item posting """
        dict = {}
        dict['id'] = self.id
        dict['traceId'] = self.traceId
        dict['itemID'] = self.itemID
        dict['sellerID'] = self.sellerID
        dict['maxCount'] = self.maxCount
        dict['minPrice'] = self.minPrice
        dict['instaBuyPrice'] = self.instaBuyPrice
        dict['closingTime'] = self.closingTime
        dict['date_created'] = self.date_created
        dict['description'] = self.description

        return dict
