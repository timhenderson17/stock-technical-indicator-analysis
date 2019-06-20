# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.firefox.options import Options
from nyse100 import nyse100
from nasdaq100 import nasdaq100
from sqlite3 import Error
import unittest, time, re, sqlite3, datetime

date = datetime.datetime.now().strftime("%Y-%m-%d")
date2 = (date,)

def create_new_entry(conn, date) :
    sql = "INSERT OR IGNORE INTO tiBuy(DATE) VALUES(\"" + date + "\");"
    cur = conn.cursor()
    cur.execute(sql)
    print(sql)
    conn.commit()
    return cur.lastrowid

def add_to_db(conn, table, co, val, date) :
    sql = "UPDATE " + table + " SET " + co + " = " + str(val) + " WHERE DATE = \"" + date + "\";"
    cur = conn.cursor()
    cur.execute(sql)
    print(sql)
    conn.commit()
    return cur.lastrowid 

def exists(conn, co, date) :
    sql = "SELECT " + co + " FROM tiBuy WHERE DATE = \"" + date + "\";"
    cur = conn.cursor()
    cur.execute(sql)
    (res,) = cur.fetchone()
    print(co + " " + str(res))
    return res

def close_data_survey(self) :
    x = 0
    try: 
        self.driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[1]/ii').click()
    except: x = 1
    try:
        self.driver.find_element_by_xpath('/html/body/div[6]/div[2]/i').click()
    except: x = 2
    try:
        self.driver.find_element_by_class('newButton Orange').click()
    except: x = 3
    try:
        self.driver.find_element_by_class('userDataPopup js-userDataPopup').click()
    except: x = 4
    return x


class BuySellForCompany(unittest.TestCase) :
    def setUp(self) :
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options = options)
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.investing.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
        create_new_entry(conn, date)

    def test_buy_sell_for_companies(self) :
        driver = self.driver
        # nyse100
        for i in range(0, len(nyse100) - 1) :
            if exists(conn, nyse100[i].replace("-", ""), date) is None :
                driver.get("https://www.investing.com/equities/" + nyse100[i] + "-technical")
                try:
                    driver.find_element_by_xpath("/html/body/div[5]/section/div[8]/ul/li[8]/a").click()
                except: # catches any exception, selenium will throw many if it can't clock on an element
                    driver.get("https://www.investing.com/equities/" + nyse100[i] + "-technical")
                    close_data_survey(self)
                    driver.find_element_by_xpath("/html/body/div[5]/section/div[8]/ul/li[8]/a").click()

                tiBuy_clean = driver.find_element_by_id("tiBuy").text.replace("(", "").replace(")", "")
                tiBuy = int("0" + tiBuy_clean)
                tiSell_clean = driver.find_element_by_id("tiSell").text.replace("(", "").replace(")", "")
                tiSell = int("0" + tiSell_clean)
                maBuy_clean = driver.find_element_by_id("maBuy").text.replace("(", "").replace(")", "")
                maBuy = int("0" + maBuy_clean)
                maSell_clean = driver.find_element_by_id("maSell").text.replace("(", "").replace(")", "")
                maSell = int("0" + maSell_clean)
                price_clean = driver.find_element_by_id("last_last").text.replace("(", "").replace(")", "")
                price = float("0" + price_clean.replace(",",""))

                add_to_db(conn, "tiBuy", nyse100[i].replace("-", ""), tiBuy, date)
                add_to_db(conn, "tiSell", nyse100[i].replace("-", ""), tiSell, date)
                add_to_db(conn, "maBuy", nyse100[i].replace("-", ""), maBuy, date)
                add_to_db(conn, "maSell", nyse100[i].replace("-", ""), maSell, date)
                add_to_db(conn, "Price", nyse100[i].replace("-", ""), price, date)

                print(nyse100[i] + ": " + str(tiBuy))
        # nasdaq100
        for i in range(0, len(nasdaq100) - 1) :
            if exists(conn, nasdaq100[i].replace("-",""), date) is None :
                driver.get("https://www.investing.com/equities/" + nasdaq100[i] + "-technical")
                try: # try clicking on weekly indicators
                    driver.find_element_by_xpath("/html/body/div[5]/section/div[8]/ul/li[8]/a").click()

                    tiBuy_clean = driver.find_element_by_id("tiBuy").text.replace("(", "").replace(")", "")
                    tiBuy = int("0" + tiBuy_clean)
                    tiSell_clean = driver.find_element_by_id("tiSell").text.replace("(", "").replace(")", "")
                    tiSell = int("0" + tiSell_clean)
                    maBuy_clean = driver.find_element_by_id("maBuy").text.replace("(", "").replace(")", "")
                    maBuy = int("0" + maBuy_clean)
                    maSell_clean = driver.find_element_by_id("maSell").text.replace("(", "").replace(")", "")
                    maSell = int("0" + maSell_clean)
                    price_clean = driver.find_element_by_id("last_last").text.replace("(", "").replace(")", "")
                    price = float("0" + price_clean.replace(",",""))

                    add_to_db(conn, "tiBuy", nasdaq100[i].replace("-", ""), tiBuy, date)
                    add_to_db(conn, "tiSell", nasdaq100[i].replace("-", ""), tiSell, date)
                    add_to_db(conn, "maBuy", nasdaq100[i].replace("-", ""), maBuy, date)
                    add_to_db(conn, "maSell", nasdaq100[i].replace("-", ""), maSell, date)
                    add_to_db(conn, "Price", nasdaq100[i].replace("-", ""), price, date)

                    print(nasdaq100[i] + ": " + tiBuy.replace("(", "").replace(")", ""))
                except: # catches any exception, selenium will throw many if it can't clock on an element
                    try: # try again for second time
                        if exists(conn, nasdaq100[i].replace("-",""), date) is None :
                            close_data_survey(self)
                            driver.find_element_by_xpath("/html/body/div[5]/section/div[8]/ul/li[8]/a").click()

                            tiBuy_clean = driver.find_element_by_id("tiBuy").text.replace("(", "").replace(")", "")
                            tiBuy = int("0" + tiBuy_clean)
                            tiSell_clean = driver.find_element_by_id("tiSell").text.replace("(", "").replace(")", "")
                            tiSell = int("0" + tiSell_clean)
                            maBuy_clean = driver.find_element_by_id("maBuy").text.replace("(", "").replace(")", "")
                            maBuy = int("0" + maBuy_clean)
                            maSell_clean = driver.find_element_by_id("maSell").text.replace("(", "").replace(")", "")
                            maSell = int("0" + maSell_clean)
                            price_clean = driver.find_element_by_id("last_last").text.replace("(", "").replace(")", "")
                            price = float("0" + price_clean.replace(",",""))

                            add_to_db(conn, "tiBuy", nasdaq100[i].replace("-", ""), tiBuy, date)
                            add_to_db(conn, "tiSell", nasdaq100[i].replace("-", ""), tiSell, date)
                            add_to_db(conn, "maBuy", nasdaq100[i].replace("-", ""), maBuy, date)
                            add_to_db(conn, "maSell", nasdaq100[i].replace("-", ""), maSell, date)
                            add_to_db(conn, "Price", nasdaq100[i].replace("-", ""), price, date)

                    except: # catches any exception, selenium will throw many if it can't clock on an element
                        continue
    def tearDown(self) :
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
 
def create_connection(db_file):
    # create a database connection to a SQLite database
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None
    
conn = create_connection("/home/timothy/financial/db/stock_ratings.db")

if __name__ == '__main__' :
    # conn = create_connection("/home/timothy/financial/stock_ratings.db")
    # if conn is not None :
    unittest.main()
        # create_new_entry(conn, date2)
    #else :
    #    print("Error: No DB connection")
