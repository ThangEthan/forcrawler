#!/bin/zsh
export PATH=/home/uh/anaconda3/bin:$PATH
export PATH=/home/uh/anaconda3/bin/scrapy:$PATH
source ~/anaconda3/etc/profile.d/conda.sh
#conda init zsh
conda activate base
cd ~/funda-sold
echo "DELETE VERKOCHT IN URL"
mysql --login-path=server -s -N scraping_data -e "UPDATE link_compare SET url = REPLACE(url, 'verkocht/','');"
echo "CREATE NEW TABLE"
mysql --login-path=server -s -N scraping_data -e "create table link_compare_sold as select * from link_compare where url in (select url from funda where sold = 'False');"
echo "Delete and readd ID"
mysql --login-path=server -s -N scraping_data -e "ALTER TABLE link_compare_sold DROP ID; ALTER TABLE link_compare_sold ADD ID INT NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (ID), AUTO_INCREMENT=1"

count=$(mysql --login-path=server -s -N scraping_data -e "SELECT min(ID) FROM link_compare_sold")
max=$(mysql --login-path=server -s -N scraping_data -e "SELECT max(ID) FROM link_compare_sold")
~/refresh_vpn.sh
while [ $count -le $max ];
do
	~/parse.sh $count funda_sold link_compare_sold
	count=$((count+1))
done
echo "Truncate table, scraping finished"
mysql --login-path=server -s -N scraping_data -e "DROP TABLE link_compare_sold; TRUNCATE link_compare;"
