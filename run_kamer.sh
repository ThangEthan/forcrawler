#!/bin/zsh
nordvpn c
echo $(date '+[%d:%m:%Y] %H:%M'): Start kamer >> ~/cron.log
cd ~/kamer-master

db_size=$(mysql --login-path=server -s -N scraping_data -e "select max(Id) from kamer;")
echo $(date '+%d_%m_%Y_%H_%M  ')$db_size >> kamer_max_prev_id.txt

echo "Updating active status, adding rented date"
mysql --login-path=server -s -N scraping_data -e "update kamer set active = 0, RentedSince = CURDATE() where active = 1;"

scrapy crawl kamer

#echo "Update duplicate in kamer_owner" 
#mysql --login-path=server -s -N scraping_data -e "UPDATE kamer_owner AS a INNER JOIN (SELECT MIN(id) AS id, sellerurl FROM kamer_owner GROUP BY sellerurl HAVING COUNT(sellerurl) > 1) AS b ON a.id > b.id AND a.SellerUrl = b.sellerurl SET a.SellerPhone = (SELECT t.sellerphone FROM (SELECT * FROM kamer_owner) AS t WHERE id = b.id), a.Achternaam = (SELECT t.Achternaam FROM (SELECT * FROM kamer_owner) AS t WHERE id = b.id), a.ActiveIn = (SELECT t.ActiveIn FROM (SELECT * FROM kamer_owner) AS t WHERE id = b.id), a.CompanyName = (SELECT t.CompanyName FROM (SELECT * FROM kamer_owner) AS t WHERE id = b.id), a.Email = (SELECT t.Email FROM (SELECT * FROM kamer_owner) AS t WHERE id = b.id), a.KVK = (SELECT t.KVK FROM (SELECT * FROM kamer_owner) AS t WHERE id = b.id), a.Note = (SELECT t.Note FROM (SELECT * FROM kamer_owner) AS t WHERE id = b.id), a.Plaats = (SELECT t.Plaats FROM (SELECT * FROM kamer_owner) AS t WHERE id = b.id), a.Typeaanbieder = (SELECT t.Typeaanbieder FROM (SELECT * FROM kamer_owner) AS t WHERE id = b.id), a.Voornaam = (SELECT t.Voornaam FROM (SELECT * FROM kamer_owner) AS t WHERE id = b.id), a.Website = (SELECT t.Website FROM (SELECT * FROM kamer_owner) AS t WHERE id = b.id);"

#echo "Delete duplicate in kamer_owner"
#mysql --login-path=server -s -N scraping_data -e "delete a from kamer_owner a inner join (select max(id) as Id, sellerurl from kamer_owner group by sellerurl having count(sellerUrl) > 1) b on a.Id < b.Id and a.SellerUrl=b.SellerUrl;"

#echo "Delete duplicate in kamer"
#mysql --login-path=server -s -N scraping_data -e "delete a from kamer a inner join (select max(Id) as Id, url  from kamer group by Url having count(url) > 1)b on a.Id < b.Id and a.url=b.url;"

#echo "Delete and readd ID"
#mysql --login-path=server -s -N scraping_data -e "ALTER TABLE kamer_owner DROP COLUMN Id; ALTER TABLE kamer_owner ADD ID INT NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY  KEY (ID), AUTO_INCREMENT=1;"

#echo "Delete and readd ID"
#mysql --login-path=server -s -N scraping_data -e "ALTER TABLE kamer DROP COLUMN Id; ALTER TABLE kamer ADD ID INT NOT NULL AUTO_INCREMENT FIRST, ADD PRIMARY  KEY (ID), AUTO_INCREMENT=1;"

echo "Add postcode"
mysql --login-path=server -s -N scraping_data -e "update kamer set postcode = (select postcode from postcode where kamer.street = street and kamer.city = city) where kamer.postcode is null;"
   
~/get_postcodes.sh
echo "Save postcode"
mysql --login-path=server -s -N scraping_data -e "drop table postcode;"
mysql --login-path=server -s -N scraping_data -e "create table postcode as (select distinct street, city, postcode from kamer);"
mysql --login-path=server -s -N scraping_data -e "truncate update_contact; truncate new_contact;"
nordvpn d
#echo "Backup data"
#mysqldump --login-path=server scraping_data kamer > ~/kamer_backups/kamer_$(date '+%d_%m_%Y_%H_%M').sql
#mysqldump --login-path=server scraping_data kamer_owner > ~/kamer_backups/kamer_owner_$(date '+%d_%m_%Y_%H_%M').sql
echo $(date '+[%d:%m:%Y] %H:%M'): Finish running kamer >> ~/cron.log
