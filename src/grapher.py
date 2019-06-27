import dateutil
from nyse100 import nyse100
from nasdaq100 import nasdaq100
from sqlite3 import Error
from dateutil import parser
import matplotlib
import matplotlib.dates as mdates
from matplotlib.dates import date2num
import matplotlib.pyplot as plt
import sqlite3, itertools

def create_connection(db_file):
    # create a database connection to a SQLite database
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def retrieve_data(query, table) :
    sql = "SELECT " + query + " FROM " + table
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    ret = []

    for row in data :
        print(row[0])
        ret.append(parser.parse(row[0])) if query == "date" else ret.append(row[0])
        
    return ret

conn = create_connection("/home/timothy/financial/db/stock_ratings.db")

companies = [nyse100, nasdaq100]
#for co in itertools.chain(*companies) :

co = nasdaq100[1].replace("-","").replace(",","").replace(".","")

tiSell = retrieve_data(co, "tiSell")
tiBuy = retrieve_data(co, "tiBuy")
maSell = retrieve_data(co, "maSell")
maBuy = retrieve_data(co, "maBuy")
price = retrieve_data(co, "Price")

dates_pre = retrieve_data("Date", "Price")
#dates = [date2num(t) for t in dates_pre]
#print(dates_pre[0])

fig = plt.figure()
heading = fig.add_subplot(111)
heading.set_title("Ratings and Price")

# Configure x-ticks
heading.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

# Plot temperature data on left Y axis
heading.set_ylabel("Rating")
heading.plot_date(dates_pre, tiSell, '-', label="tiSell", color='r')
heading.plot_date(dates_pre, tiBuy, '-', label="toBuy", color='b')

# Plot humidity data on right Y axis
ax2 = heading.twinx()
ax2.set_ylabel("Price")
ax2.plot_date(dates_pre, price, '-', label="Price", color='g')

# Format the x-axis for dates (label formatting, rotation)
fig.autofmt_xdate(rotation=60)
fig.tight_layout()

# Show grids and legends
heading.grid(True)
heading.legend(loc='best', framealpha=0.5)
ax2.legend(loc='best', framealpha=0.5)

plt.savefig("figure.png")




    