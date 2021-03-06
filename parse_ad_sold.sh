#!/bin/zsh
# This script goes through all link scraped by parselink.sh and scrape its content
export PATH=/home/uh/anaconda3/bin:$PATH
export PATH=/home/uh/anaconda3/bin/scrapy:$PATH
source ~/anaconda3/etc/profile.d/conda.sh
#conda init zsh
conda activate base
cd ~/funda-sold
echo "DELETE VERKOCHT IN URL"
# This make all links in database have the same format
mysql --login-path=server -s -N scraping_data -e "UPDATE link_compare SET url = REPLACE(url, 'verkocht/','');"
echo "CREATE NEW TABLE"
# Put links into new table if that link's status found to be available in the database
mysql --login-path=server -s -N scraping_data -e "create table link_compare_sold as select * from link_compare where url in (select url from funda where sold = 'False');" # Need more elegant way
echo "Delete and readd ID"
mysql --login-path=server -s -N scraping_data -e "ALTER TABLE link_compare_sold DROP ID; ALTER TABLE link_compare_sold ADD ID INT NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (ID), AUTO_INCREMENT=1"

count=$(mysql --login-path=server -s -N scraping_data -e "SELECT min(ID) FROM link_compare_sold")
max=$(mysql --login-path=server -s -N scraping_data -e "SELECT max(ID) FROM link_compare_sold")
~/refresh_vpn.sh
while [ $count -le $max ];
do
	~/parse.sh $count funda_sold link_compare_sold # Scraping content
	count=$((count+1))
done
echo "Truncate table, scraping finished"
mysql --login-path=server -s -N scraping_data -e "DROP TABLE link_compare_sold; TRUNCATE link_compare;"
