#!/bin/sh

FILES="401307_city_fukuoka_covid19_exam"

for F in $FILES
do
    echo "cat ${F}.csv | nkf --oc=utf-8 > ${F}_utf8.csv"
          cat ${F}.csv | nkf --oc=utf-8 > ${F}_utf8.csv
done
