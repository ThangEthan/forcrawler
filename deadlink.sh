#!/bin/zsh
# This script detect dead link of houses are with status Available in database, then change its status to Deleted
# This script should be run after parselink.sh 1 lastpage beschikbaar/sorteer-datum-af (scrape every available house links)
count=0
while read link
do
    echo "Checking $link"
    line=$(timeout 10 lynx -connect_timeout=10 --source $link > ~/house/some_random_house.html | wc -l)
    while [[ $line -lt 300 ]]; # bad response goes here
    do
        echo "Retrying. Refreshing vpn connection"
        ~/refresh_vpn.sh
        line=$(timeout 10 lynx -connect_timeout=10 --source $link > ~/house/some_random_house.html | wc -l)
    done
    if [[ $line -gt 8000 ]] # you need to find the right number
    then
        echo "Dead link detected"
        mysql --login-path=server -s -N scraping_data -e "update funda set Status = 'Deleted' where Url = '$link';"
    fi
    count=$((count+1))
    nordvpn_refresh=$count%3
    if [[ $nordvpn_refresh -eq 0 ]]
    then
        echo "Refreshing vpn connection"
        ~/refresh_vpn.sh > /dev/null 2>&1
    fi
done < <(mysql --login-path=server -s -N scraping_data -e "select f.url from funda f left join link_compare l on f.url = l.url where l.url is null and f.Status = 'Beschikbaar';") # Test links in the database that aren't appear in all the scraped link. Some links still active but doesn't appear on the list
