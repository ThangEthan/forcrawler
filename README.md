This respo contains all the necessary shell script and scraper to run crawler
FUNDA workflow:
    parselink.sh run first store all house link from a page into ~/house/link.txt, then database will import those link to table link_compare
    parse_ad_sell.sh then run. Delete all link that are already in the database to ensure no duplicate. Then it will go through all link in link_compare to download the html doc, save it into ~/house/some_random_house.html. Finally, the scraper will extract all the info, save it into the database
    parselink.sh will run again store all house from sold page into ~/house/link.txt, then database will import those link to table link_compare, then create a new table called link_compare_sold which hold all house that in the database AND have available status
    parse_ad_sold.sh then run. Goes through link in link_compare_sold. Extracting the date it was sold and how long it has been on the flatform
    parse_reserve.sh then run. It goes through all the reserved pages. Extracting link and its status and store it in a table named reserved. Then will update existing link in the database with the scraped status
    get_cor.sh then run it form a string from address and postcode of an record in the database, then search for the location coordinate in WOZ. Finally, add those in the row record

Kamer workflow:
    First we set every active house to inactive, and add today as the date it become inactive.
    Then run the scraper, it will scrape every ad on the platform and check if the ad url is in the database or not. If it is, then set that ad to be active again and remove the date it become inactive (added in the first step)
    Finally, get_postcode.sh run. Searching WOZ for the ad postcode. Although, the scraped postcode is not 100% correct as kamernet only have the street name and postcode to search from.

Pararius workflow:
    Is similar to Kamernet's