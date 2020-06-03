#!/bin/zsh
# This script goes through all scraped link by parselink.sh and scrape its content
export PATH=/home/uh/anaconda3/bin:$PATH
export PATH=/home/uh/anaconda3/bin/scrapy:$PATH
#conda init bash
source ~/anaconda3/etc/profile.d/conda.sh
conda activate base
cd ~/funda-master
#echo "Checking for back on sell house"
#mysql --login-path=server -s -N scraping_data -e "INSERT INTO resell SELECT * FROM funda WHERE funda.url IN (SELECT url FROM link_compare) AND sold  = 'True';"
#echo "Update house status"
#mysql --login-path=server -s -N scraping_data -e "UPDATE funda AS f INNER JOIN link_compare ON f.url = link_compare.url SET f.sold = 'False', f.Verkoopdatum = null, f.status='Beschikbaar' WHERE f.sold = 'True';"
echo "Delete duplicate"
# Delete link that already in the database or in wrong format
mysql --login-path=server -s -N scraping_data -e "SET SQL_SAFE_UPDATES=0; DELETE link_compare FROM link_compare INNER JOIN funda on funda.url=link_compare.url; DELETE FROM link_compare where url like 'https://www.funda.nl/%huur%';"
echo "Delete and readd ID"
mysql --login-path=server -s -N scraping_data -e "ALTER TABLE link_compare DROP ID; ALTER TABLE link_compare ADD ID INT NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY  KEY (ID), AUTO_INCREMENT=1"

count=$(mysql --login-path=server -s -N scraping_data -e "SELECT min(ID) FROM link_compare")
max=$(mysql --login-path=server -s -N scraping_data -e "SELECT max(ID) FROM link_compare")
~/refresh_vpn.sh
while [ $count -le $max ];
do
	~/parse.sh $count funda link_compare # Scraping content
	count=$((count+1))
done
echo "Truncate table, scraping finished"
mysql --login-path=server -s -N scraping_data -e "TRUNCATE TABLE link_compare"
