import mysql.connector
db_conn = mysql.connector.connect(host="34.220.52.212", user="root",
password="NewPassword", database="auctiondb")
db_cursor = db_conn.cursor()
db_cursor.execute('''
DROP TABLE bid_Auction, post_Auction
''')
db_conn.commit()
db_conn.close()