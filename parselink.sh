#!/bin/zsh
# This script will save all the link in database base on given condition/filter. These condition/filter can be found in the link on funda. Ex: https://www.funda.nl/koop/heel-nederland/beschikbaar/nieuwbouw/sorteer-datum-af/ 
# $1, $2: from page to page
# $3: condition/filter
~/refresh_vpn.sh
sleep 1

for i in {$1..$2}
do
	echo "Parsing page $i"
	line=$(timeout 10 lynx -connect_timeout=10 -listonly -nonumbers -dump https://www.funda.nl/$3/heel-nederland/$4/p$i/ | awk '/Hidden links:/,0' | grep -e "https\:\/\/www.funda.nl\/\(koop\|huur\)\/.*" | grep -P '^(?!.*\/p[0-9].*).*$' > ~/house/link.txt | wc -l)
	echo "$line results" # expected to have 15
	while [[ $line -eq 0 ]] ; do # redo if doesn't
		echo "Retrying"
		~/refresh_vpn.sh
		sleep 0.5
		echo "Parsing page $i"
        	line=$(timeout 10 lynx -connect_timeout=10 -listonly -nonumbers -dump https://www.funda.nl/$3/heel-nederland/$4/p$i/ | awk '/Hidden links:/,0' | grep -e "https\:\/\/www.funda.nl\/\(koop\|huur\)\/.*" | grep -P '^(?!.*\/p[0-9].*).*$' > ~/house/link.txt | wc -l)
		echo "$line results"
	done
	mysql --login-path=server --local-infile=1 scraping_data -e "LOAD DATA LOCAL INFILE '/home/crawler1/house/link.txt' IGNORE INTO TABLE link_compare (url);" # save to database
	nordvpn_refresh=$i%3 # refresh VPN every 3 page
	if [[ $nordvpn_refresh -eq 0 ]]
	then
		echo "Refreshing vpn connection"
		~/refresh_vpn.sh
		sleep 0.5
	else
		sleep 0.5
	fi
done

