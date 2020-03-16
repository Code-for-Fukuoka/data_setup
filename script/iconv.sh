#!/bin/sh

# FILES="401307_city_fukuoka_covid19_hotline
# 401307_city_fukuoka_covid19_patients
# 401307_city_fukuoka_covid19_visit"
# FILES="401307_city_fukuoka_covid19_exam"

for F in $FILES
do
    echo $F
    iconv --from-code=shift-jis --to-code=utf8 -o ${F}_utf8.csv ${F}.csv
done

