#!/bin/zsh
~/refresh_vpn.sh
sleep 1

for i in {$1..$2}
do
	echo "Parsing page $i"
	line=$(timeout 10 lynx -connect_timeout=10 -listonly -nonumbers -dump https://www.funda.nl/$3/heel-nederland/$4/p$i/ | awk '/Hidden links:/,0' | grep -e "https\:\/\/www.funda.nl\/\(koop\|huur\)\/.*" | grep -P '^(?!.*\/p[0-9].*).*$' > ~/house/link.txt | wc -l)
	echo "$line results"
	while [[ $line -eq 0 ]] ; do
		echo "Retrying"
		~/refresh_vpn.sh
		sleep 0.5
		echo "Parsing page $i"
        	line=$(timeout 10 lynx -connect_timeout=10 -listonly -nonumbers -dump https://www.funda.nl/$3/heel-nederland/$4/p$i/ | awk '/Hidden links:/,0' | grep -e "https\:\/\/www.funda.nl\/\(koop\|huur\)\/.*" | grep -P '^(?!.*\/p[0-9].*).*$' > ~/house/link.txt | wc -l)
		echo "$line results"
	done
	mysql --login-path=server --local-infile=1 scraping_data -e "LOAD DATA LOCAL INFILE '/home/crawler1/house/link.txt' IGNORE INTO TABLE link_compare (url);"
	nordvpn_refresh=$i%3
	if [[ $nordvpn_refresh -eq 0 ]]
	then
		echo "Refreshing vpn connection"
		~/refresh_vpn.sh
		sleep 0.5
	else
		sleep 0.5
	fi
done

