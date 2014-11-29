CheckManga
==========

A simple web scraper script that checks manga fox to see if any of the manga I've been reading has been updated. Also generates a database of the manga I'm reading and updates itself whenever the web scraper finds a new chapter has been released.

Notes for improvement:
-Interactions with the database are the slowest part. Currently, retrieving a title from the db, checking for updates, and then commiting changes back to the db. Simply loading the entire DB first, making necessary updates, and then writing it all back at the same time would likely be much faster.

-Some redundant or non-helpful functionality still in there.

-Web scraping and db-functionalities need to be separated a bit more.
