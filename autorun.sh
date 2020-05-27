#!/bin/zsh
echo $(date '+[%d:%m:%Y] %H:%M'): Start funda >> ~/cron.log
~/parselink.sh $1 $2 koop beschikbaar/sorteer-datum-af
~/parse_ad_sell.sh
~/parselink.sh $1 $2 koop verkocht/sorteer-datum-af
~/parse_ad_sold.sh
~/parse_reserved.sh $1 $2

~/parselink.sh 1 300 huur
~/parse_ad_rent.sh
~/parselink.sh 1 300 huur verhuurd
~/parse_ad_rented.sh
echo $(date '+[%d:%m:%Y] %H:%M'): Finished running funda >> ~/cron.log
#mysqldump --login-path=local scraping_data funda > ~/funda_sell_backups/funda_$(date '+%d_%m_%Y_%H_%M').sql
#mysqldump --login-path=local scraping_data fundarent > ~/fundarent_backups/fundarent_$(date '+%d_%m_%Y_%H_%M').sql
