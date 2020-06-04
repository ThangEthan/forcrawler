This respo contains all the necessary shell script and scraper to run crawler
FUNDA workflow:
    parselink.sh run first store all house link from a page into ~/house/link.txt, then database will import those link to table link_compare
    parse_ad_sell.sh then run. Delete all link that are already in the database to ensure no duplicate. Then it will go through all link in link_compare to download the html doc, save it into ~/house/some_random_house.html. Finally, the scraper will extract all the info, save it into the database
    