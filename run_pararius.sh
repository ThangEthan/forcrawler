#!/bin/zsh
#runs the pararius_rent scraper and updates the database accordingly
#eval "$(conda shell.zsh hook)"
#conda activate scraping_env
echo $(date '+[%d:%m:%Y] %H:%M'): Run pararius >> ~/cron.log
cd ~/UH-master 

timeout 30 nordvpn c de

while [[ $? -eq 1  ]]
do 
	timeout 30 nordvpn c de
done

echo "COLUMNS TO TEXT"
mysql --login-path=server -s -N scraping_data -e "alter table pararius change column Postalcode Postalcode TEXT NULL DEFAULT NULL; alter table pararius change column Squaremeters Squaremeters TEXT NULL DEFAULT NULL; alter table pararius change column Rentpermonth Rentpermonth TEXT NULL DEFAULT NULL;"
mysql --login-path=server -s -N scraping_data -e "update pararius set active = 0, rentedsince = CURDATE() where active = 1"
size=$(mysql --login-path=server -s -N scraping_data -e "select max(Id) from pararius;")

echo "SCRAPE"
scrapy crawl house 

echo "DELETE DUP, COLUMNS TO INT"
mysql --login-path=server -s -N scraping_data -e "ALTER TABLE pararius_owner DROP COLUMN Id; ALTER TABLE pararius_owner ADD COLUMN Id INT NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (Id), ADD UNIQUE INDEX Id_UNIQUE (Id ASC) VISIBLE; ALTER TABLE pararius DROP COLUMN Id; ALTER TABLE pararius ADD COLUMN Id INT NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY KEY (Id), ADD UNIQUE INDEX Id_UNIQUE (Id ASC) VISIBLE; update pararius set Squaremeters = NULL WHERE Squaremeters = ''; update pararius set Rentpermonth = null where Rentpermonth = 'Price on request'; update pararius set Rentpermonth = null where Rentpermonth = ''; update pararius set Postalcode = null where Postalcode = ''; alter table pararius change column Postalcode Postalcode INT NULL DEFAULT NULL; alter table pararius change column Squaremeters Squaremeters INT NULL DEFAULT NULL; alter table pararius change column Rentpermonth Rentpermonth INT NULL DEFAULT NULL; update pararius set Availablefrom = DATE_FORMAT(CURDATE(), '%d-%m-%Y') where Availablefrom = 'Immediately';"

nordvpn d
#echo "Backup data"
#mysqldump --login-path=server scraping_data pararius > ~/pararius_rent_backups/pararius_$(date '+%d_%m_%Y_%H_%M').sql
#mysqldump --login-path=server scraping_data pararius_owner > ~/pararius_owner_backups/pararius_owner_$(date '+%d_%m_%Y_%H_%M').sql
echo $(date '+[%d:%m:%Y] %H:%M'): Finish running pararius >> ~/cron.log
