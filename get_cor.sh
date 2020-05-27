#!/bin/zsh
RED='\033[0;31m'
NC='\033[0m'

function req(){
    adres_id=$(curl -m 5 "https://www.wozwaardeloket.nl/api/geocoder/v3/suggest?query=$line" -H 'Sec-Fetch-Mode: cors' -H 'Sec-Fetch-Site: same-origin' -H 'Accept-Encoding: gzip, deflate, br' -H 'Accept-Language: en-GB,en-US;q=0.9,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36' -H 'Accept: */*' -H 'Referer: https://www.wozwaardeloket.nl/index.jsp' -H 'X-Requested-With: XMLHttpRequest' -H 'Cookie: stg_returning_visitor=Fri, 02 Aug 2019 14:33:40 GMT; _63a62=http://10.0.0.100:8080; JSESSIONID=1EA8531E2A4DFA8D4B9A4DC37EF5EBF0; stg_traffic_source_priority=1; _pk_ses.49d516ae-c5e9-11e7-aae6-0017fa104e46.b995=*; stg_externalReferrer=https://www.wozwaardeloket.nl/index.jsp; _pk_id.49d516ae-c5e9-11e7-aae6-0017fa104e46.b995=192e4055a8cdb41a.1564749328.13.1567598507.1567598505.; stg_last_interaction=Wed, 04 Sep 2019 12:02:02 GMT' -H 'Connection: keep-alive' --compressed | jq -r '.docs | [.[] | select(.type == "adres")] | .[0] | .id')

    read x y <<< $(curl -m 10 "https://www.wozwaardeloket.nl/api/geocoder/v3/lookup?id=$adres_id" -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://www.wozwaardeloket.nl/index.jsp' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Cookie: _pk_ses.49d516ae-c5e9-11e7-aae6-0017fa104e46.b995=*;_pk_id.49d516ae-c5e9-11e7-aae6-0017fa104e46.b995=16e9735b97e3f285.1582641907.1.1582641907.1582641907.;stg_last_interaction=Tue%2C%2025%20Feb%202020%2014:45:07%20GMT;stg_traffic_source_priority=1;stg_returning_visitor=Tue%2C%2025%20Feb%202020%2014:45:07%20GMT;JSESSIONID=E949982C3D532BD5F58B1202FCF1363F;_63a62=http://10.0.0.120:8080;' | jq -r '[.centroide_ll.x, .centroide_ll.y] | @tsv')

}

while read row
do
    id=$(echo $row | cut -f1)
    line=$(echo $row | cut -f2 )
    echo "${RED}$id${NC}"
    req
    sleep 1 
    if [[ ! -z $x ]];
    then
        mysql --login-path=server -s -N scraping_data -e "UPDATE funda SET x = '$x' , y = '$y'  WHERE id = '$id';"
    else 
        mysql --login-path=server -s -N scraping_data -e "UPDATE funda SET x = -1 , y = -1  WHERE id = '$id';" 
    fi

done < <(mysql --login-path=server -s -N scraping_data -e "select id, URLENCODERCUR(concat(adres , ', ', postcode)) as line from funda where x is null and y is null order by id desc limit 50000;")


