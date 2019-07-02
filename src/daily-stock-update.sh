#!/bin/bash
# daily chron job for getting stock technical indicator and moving avg recommendations

cd /home/timothy/financial
source env/bin/activate
cd /home/timothy/financial/src
# python cannot catch all the errors, so sometimes it just needs restart where it left off
python3 ./BuySellForCompany.py
python3 ./BuySellForCompany.py
python3 ./BuySellForCompany.py
python3 ./BuySellForCompany.py
python3 ./BuySellForCompany.py
python3 ./BuySellForCompany.py
python3 ./BuySellForCompany.py
