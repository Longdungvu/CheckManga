CheckManga
==========

A simple web scraper that scrapes manga hosting websites to see if any of the manga I've been reading has been updated. Stores data on each title, manga hosting website, and how to scrape each site in a database. Database updates whenever the web scraper finds a new chapter has been released. Working on implementing a new "bookmarking" feature that will let me keep track of new manga I start reading where I am not yet caught up to the most recent chapter or where the series has been completed.

4/9/2015 

-Web scraper is now site independent (removed dependence on a single particular site for all of the manga scraping.)  
-Changed database schema so that there are now 3 tables in the SQLite database. (manga, sites, and tags)  
-Wrote a function to generate a database from Json files.  
-Can now add 'Completed' manga to the db which will not be scraped.  
-Distinction between LastChapterRead and MostRecentChapter now.

Useful additions:

-Being able to update, delete, or add entries in bulk rather than just one by one or being able to update, delete, or add based on a json or text file. (Can already generate a db from json files, now need functions for bulk addition or deletion (or update?) from db from a json or text file.)

-Being able to "bookmark" your most recent chapter read for a manga that is either completed or that you just started and haven't caught up to the latest chapter released. (Still need to fully implement functions. Ex. function that will query the database and Return all of the the "bookmarks" and how to bookmark/not scrape a manga title that is ongoing but where you have not yet caught up to the most recent chapter.)

-Figure out naming conventions for the column names in the db and the example json names (how to be consistent despite two different sets of rules?) Set foreign key in the tags table?
