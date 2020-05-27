#!/bin/zsh
echo "Parsing link no.$1"
link=$(mysql --login-path=local -s -N scraping_data -e "SELECT URL FROM link_compare_sold WHERE ID = $1;")
line=$(timeout 10 lynx --source $link > ~/house/some_random_house.html | wc -l)
while [[ $line -lt 300 ]]; # bad response goes here
do
        echo "Retrying. Refreshing vpn connection"
        ~/refresh_vpn.sh
        line=$(timeout 10 lynx -connect_timeout=10 --source $link > ~/house/some_random_house.html | wc -l)
done

scrapy crawl $2
nordvpn_refresh=$1%3
if [[ $nordvpn_refresh -eq 0 ]]
then
        echo "Refreshing vpn connection"
        ~/refresh_vpn.sh
fi
mysql --login-path=local -s -N scraping_data -e "DELETE FROM link_compare_sold where ID = $1"

