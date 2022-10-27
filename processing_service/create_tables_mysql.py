import sqlite3

conn = sqlite3.connect('stats.sqlite')

c = conn.cursor()
c.execute('''
            CREATE TABLE stats
            (id INTEGER PRIMARY KEY ASC,
            num_bids INTEGER NOT NULL,
            max_bid INTEGER NOT NULL,
            num_items_listed INTEGER NOT NULL,
            max_instabuy_price INTEGER(100) NOT NULL,
            last_updated VARCHAR(100) NOT NULL,
            traceID STRING(100) NOT NULL)
          ''')

conn.commit()
conn.close()

