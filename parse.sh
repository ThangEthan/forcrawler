#!/bin/zsh
# This script scrape the content of an ad base on given scraper name, table name, row id
# $1: link id
# $2: scraper name
# $3: table contains links
echo "Parsing link no.$1"
link=$(mysql --login-path=server -s -N scraping_data -e "SELECT URL FROM $3 WHERE ID = $1;") # Take the link from the given table name
line=$(timeout 10 lynx -connect_timeout=10 --source $link > ~/house/some_random_house.html | wc -l)
while [[ $line -lt 300 ]]; # bad response goes here
do
	echo "Retrying. Refreshing vpn connection"
	~/refresh_vpn.sh
	line=$(timeout 10 lynx -connect_timeout=10 --source $link > ~/house/some_random_house.html | wc -l)
done

scrapy crawl $2 > /dev/null 2>&1
nordvpn_refresh=$1%3
if [[ $nordvpn_refresh -eq 0 ]]
then
	echo "Refreshing vpn connection"
	~/refresh_vpn.sh
fi
mysql --login-path=server -s -N scraping_data -e "DELETE FROM $3 where ID = $1"
