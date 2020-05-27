#!/bin/zsh
export PATH=/home/uh/anaconda3/bin:$PATH
#conda init zsh
source ~/anaconda3/etc/profile.d/conda.sh
conda activate base
cd ~/funda_rent
echo "Update house status"
mysql --login-path=server -s -N scraping_data -e "UPDATE fundarent AS f INNER JOIN link_compare ON f.url = link_compare.url SET f.rented = 'False', f.Verhuurdatum = null, f.status='Beschikbaar' WHERE f.rented = 'True';"
echo "Delete duplicate"
mysql --login-path=server -s -N scraping_data -e "DELETE link_compare FROM link_compare INNER JOIN fundarent on fundarent.url=link_compare.url AND fundarent.rented = 'False';"
echo "Delete and readd ID"
mysql --login-path=server -s -N scraping_data -e "ALTER TABLE link_compare DROP ID; ALTER TABLE link_compare ADD ID INT NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY  KEY (ID), AUTO_INCREMENT=1"

count=$(mysql --login-path=server -s -N scraping_data -e "SELECT min(ID) FROM link_compare")
max=$(mysql --login-path=server -s -N scraping_data -e "SELECT max(ID) FROM link_compare")
~/refresh_vpn.sh
while [ $count -le $max ];
do
	~/parse.sh $count funda_rent link_compare
	count=$((count+1))
done
echo "Truncate table, scraping finished"
mysql --login-path=server -s -N scraping_data -e "TRUNCATE TABLE link_compare"
