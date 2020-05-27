#!/bin/zsh
RED='\033[0;31m'
NC='\033[0m'

function req(){
    postcode=$(curl 'https://www.wozwaardeloket.nl/api/geocoder/v3/suggest?query='"$street1%20,$city1" -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://www.wozwaardeloket.nl/index.jsp' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H 'Cookie: _63a62=http://10.0.0.219:8080; JSESSIONID=5C88832DAA11D003850C55EAE07C7338; stg_returning_visitor=Thu, 22 Aug 2019 12:58:41 GMT; stg_traffic_source_priority=4; stg_externalReferrer=https://www.wozwaardeloket.nl/index.jsp; stg_last_interaction=Thu, 22 Aug 2019 12:58:41 GMT; _pk_id.49d516ae-c5e9-11e7-aae6-0017fa104e46.b995=e4e07b41de83e72b.1566478283.1.1566478692.1566478283.; _pk_ses.49d516ae-c5e9-11e7-aae6-0017fa104e46.b995=*' | jq '.docs[]'| jq '.weergavenaam' | grep -o -E ', [0-9]{4}' | grep -o -E '[0-9]+' | sort | uniq -c | sort -n -k 1 -r | head -n 1 | awk -F ' ' '{print $2}')
echo "curl 'https://www.wozwaardeloket.nl/api/geocoder/v3/suggest?query='$street1%20$city1"
}

while read row
do

    street=$(echo $row | cut -f1)
    city=$(echo $row | cut -f2 )

    street1=$(echo "${street//\"/%22}")
    street1="${street1// /%20}"
    city1="${city// /%20}"
    city1=$(echo "${city1//\"/%22}")
    req
    echo "${RED}POSTCODE: $postcode${NC}"



    mysql --login-path=server -s -N scraping_data -e "UPDATE kamer SET Postcode='"$postcode"' WHERE Street='"$street"' and City='"$city"';"

done < <(mysql --login-path=server -s -N scraping_data -e "SELECT DISTINCT Street, City FROM scraping_data.kamer where postcode IS NULL;")


