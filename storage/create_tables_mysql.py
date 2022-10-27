import mysql.connector
db_conn = mysql.connector.connect(host="ec2-35-89-159-232.us-west-2.compute.amazonaws.com", user="root",
password="NewPassword", database="auctiondb")

c = db_conn.cursor()
c.execute('''
            CREATE TABLE post_Auction
            (id INT NOT NULL AUTO_INCREMENT,
            traceId VARCHAR(100) NOT NULL,
            itemID VARCHAR(250) NOT NULL,
            sellerID VARCHAR(250) NOT NULL,
            maxCount INTEGER NOT NULL,
            minPrice INTEGER NOT NULL,
            instaBuyPrice INTEGER NOT NULL,
            closingTime VARCHAR(100) NOT NULL,
            date_created VARCHAR(100) NOT NULL,
            description VARCHAR(250) NOT NULL,
            CONSTRAINT post_Auction PRIMARY KEY (id))
          ''')

c.execute('''
            CREATE TABLE bid_Auction
            (id INT NOT NULL AUTO_INCREMENT,
            traceId VARCHAR(100) NOT NULL,
            itemID VARCHAR(250) NOT NULL,
            bidderID VARCHAR(250) NOT NULL,
            bidID VARCHAR(250) NOT NULL,
            bidCount INTEGER NOT NULL,
            bidPrice INTEGER NOT NULL,
            bidTime VARCHAR(100) NOT NULL,
            date_created VARCHAR(100) NOT NULL,
            CONSTRAINT bid_Auction PRIMARY KEY (id))

          ''')

db_conn.commit()
db_conn.close()
