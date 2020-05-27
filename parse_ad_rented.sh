#!/bin/zsh
export PATH=/home/uh/anaconda3/bin:$PATH
source ~/anaconda3/etc/profile.d/conda.sh
#conda init zsh
conda activate base
cd ~/funda_rented

echo "Update house status"
mysql --login-path=server -s -N scraping_data -e "UPDATE link_compare SET url = REPLACE(url, 'verhuurd/','');"

echo "CREATE NEW TABLE"
mysql --login-path=server -s -N scraping_data -e "create table link_compare_rented as select * from link_compare where url in (select url from fundarent where rented = 'False');"

echo "Delete and readd ID"
mysql --login-path=server -s -N scraping_data -e "ALTER TABLE link_compare_rented DROP ID; ALTER TABLE link_compare_rented ADD ID INT NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY  KEY (ID), AUTO_INCREMENT=1"

count=$(mysql --login-path=server -s -N scraping_data -e "SELECT min(ID) FROM link_compare_rented")
max=$(mysql --login-path=server -s -N scraping_data -e "SELECT max(ID) FROM link_compare_rented")
~/refresh_vpn.sh
while [ $count -le $max ];
do
	~/parse.sh $count funda_rented link_compare_rented
	count=$((count+1))
done
echo "Truncate table, scraping finished"
mysql --login-path=server -s -N scraping_data -e "DROP TABLE link_compare_rented;TRUNCATE TABLE link_compare;"
