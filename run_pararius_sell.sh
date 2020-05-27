#!/bin/zsh
#run the pararius scraper and update database accordingly
#eval "$(conda shell.zsh hook)"
#conda activate scraping_env
echo $(date '+[%d:%m:%Y] %H:%M'): Run pararius sell >> ~/cron.log
cd ~/pararius_sell
nordvpn c
size=$(mysql --login-path=server -s -N scraping_data -e "select max(Id) from pararius_sell;")

echo "UPDATE ACTIVE STATUS"
mysql --login-path=server -s -N scraping_data -e "update pararius_sell set active = 0, SoldSince = CURDATE() where active = 1;"
mysql --login-path=server -s -N scraping_data -e "update pararius_sell as p inner join (select min(Id) Id from pararius_sell where Active = 1 group by Url having count(*) = 1)pp on pp.Id = p.Id set p.Active = 0, SoldSince = CURDATE();update pararius_sell set Active = 1, SoldSince = null where Id > $size;"

echo "SCRAPE"
scrapy crawl house 

#echo "DELETE AND READ ID"
#something wrong with "
#mysql --login-path=local -s -N scraping_data -e "ALTER TABLE pararius_owner DROP COLUMN Id; ALTER TABLE pararius_owner ADD COLUMN Id INT NOT NULL AUTO_INCREMENT FIRST , ADD PRIMARY KEY (Id), ADD UNIQUE INDEX Id_UNIQUE (Id ASC) VISIBLE; ALTER TABLE pararius_sell DROP COLUMN Id; ALTER TABLE pararius_sell ADD COLUMN Id INT NOT NULL AUTO_INCREMENT, ADD PRIMARY KEY (Id), ADD UNIQUE INDEX Id_UNIQUE (Id ASC) VISIBLE;"
#nordvpn d
echo $(date '+[%d:%m:%Y] %H:%M'): Finish running pararius sell >> ~/cron.log
