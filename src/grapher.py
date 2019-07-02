import dateutil
from nyse100 import nyse100
from nasdaq100 import nasdaq100
from sqlite3 import Error
from dateutil import parser
import matplotlib
import matplotlib.dates as mdates
from matplotlib.dates import date2num
from matplotlib import gridspec
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import sqlite3, itertools

def create_connection(db_file) :
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
        ret.append(parser.parse(row[0])) if query == "date" else ret.append(row[0])
        
    return ret

conn = create_connection("/home/timothy/financial/db/stock_ratings.db")

companies = [nyse100, nasdaq100]
with PdfPages('graphs.pdf') as pdf :
    for co in itertools.chain(*companies) :

        co = co.replace("-","").replace(",","").replace(".","")

        tiSell = retrieve_data(co, "tiSell")
        tiBuy = retrieve_data(co, "tiBuy")
        maSell = retrieve_data(co, "maSell")
        maBuy = retrieve_data(co, "maBuy")
        price = retrieve_data(co, "Price")

        dates_pre = retrieve_data("Date", "Price")
        #dates = [date2num(t) for t in dates_pre]
        #print(dates_pre[0])

        fig = plt.figure(figsize=(6,8))
        gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])
        heading = fig.add_subplot(gs[0])
        heading.set_title("Ratings and Price for " + co)

        # Configure x-ticks
        heading.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

        # Plot temperature data on left Y axis
        heading.set_ylabel("Rating")
        heading.plot_date(dates_pre, tiSell, '-', label="Sell", color='r')
        heading.plot_date(dates_pre, tiBuy, '-', label="Buy", color='b')
        heading.plot_date(dates_pre, maSell, '-', color='r')
        heading.plot_date(dates_pre, maBuy, '-', color='b')

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

        # %Gain per 'sell'
        gains = [0]
        for i, p in enumerate(price) :
            if i != 0 :
                try:
                    percent_gain = (price[i] - price[i-1]) / float(price[i-1] + .001)
                    sell_ratings = tiSell[i] + maSell[i] + .001
                    gains.append(percent_gain / sell_ratings) 
                except TypeError:
                    gains.append(0)

        plt.subplot(gs[1])
        plt.plot_date(dates_pre, gains, '*', label="% Gain per Sell Rating", color='b')
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)




    