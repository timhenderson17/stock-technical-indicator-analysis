#!/bin/bash
# daily chron job for getting stock technical indicator and moving avg recommendations

cd /home/timothy/financial
source env/bin/activate
cd /home/timothy/financial/src
# python cannot catch all the errors, so sometimes it just needs restart where it left off

MY_OUTPUT="$(python3 ./BuySellForCompany.py)"
until [[ "$MY_OUTPUT" == *"SUCCESS"* ]]
do
    echo "$MY_OUTPUT"
    MY_OUTPUT="$(python3 ./BuySellForCompany.py)"
done

echo "$MY_OUTPUT"

cp /home/timothy/financial/db/daily-stock-update.sh /home/timothy/financial/db/backup.db
