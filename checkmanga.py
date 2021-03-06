from bs4 import BeautifulSoup as BSoup
import requests
import sqlite3
import sys

#'mycheckmanga.db' is the name of the exmaple database included with this code.


def db_get_entry_info(title, cur):
    """Input: Manga title, and cursor object 
    Output: Returns a dictionary of the manga's info from the db, keys to the dict are columns of the db."""
    cur.execute("SELECT * FROM manga WHERE Title = (?)", [title])
    entry = cur.fetchone()
    return dict(entry) 

def scrape_latest_chapter(url, site_path):
    """Input: A url string and a 'site_path' which is essentially a Json object. (A list of dictionaries. The dictionaries are html tags and are arranged in a specific order.)
    Output: A string scraped from the provided url that is the latest chapter of the manga at that url."""
    chapter = BSoup(requests.get(url, timeout=30).text)
    for tag in site_path:
        if tag['TagClass'] != None:
            chapter = chapter.find(tag['TagName'], {'class':tag['TagClass']})
        else:
            chapter = chapter.find(tag['TagName'])
    return chapter.text.strip()
        
def update_last_read(title, cur, con):
    """Input: The title of a manga.
    Output: None. Updates the db so that LastChapterRead = MostRecentChapter."""
    cur.execute("UPDATE manga SET LastChapterRead = MostRecentChapter WHERE Title = (?)", [title])
    con.commit()

def check_manga(cur, con, cache_dict, auto_up=True):
    """Input: The cursor object and an auto_update boolean (default=True) that tells the function whether to automatically update LastChapterRead to be the same as MostRecentChapter.
    Output: None. Updates the DB by scraping for chapters for manga where Status = 'Ongoing' and where MostRecentChapter = LastChapterRead"""
    cur.execute("SELECT * FROM manga WHERE Status = 'Ongoing'")
    all_rows = cur.fetchall()    
    for entry in all_rows:
        if cache_dict.get(entry["Site"]) != None:
            site_path = cache_dict.get(entry["Site"])
        else:
        #The SQL statement below retrieves the "site_path" (aka instructions on how to scrape that manga site) from the tags table of the db.
            cur.execute("SELECT * FROM tags WHERE site=(?) ORDER BY ID ASC", [entry['Site']])
            site_path = cur.fetchall()
            cache_dict[entry["Site"]] = site_path
        print "Currently Scraping:", entry["Title"]
        try:
            most_recent_chapter = scrape_latest_chapter(entry['Url'], site_path)
            if entry['MostRecentChapter'] != most_recent_chapter:     
                cur.execute("UPDATE manga SET MostRecentChapter = (?) WHERE Title = (?)", (most_recent_chapter,entry["Title"])) 
                print 'A new chapter has been released for ' + entry["Title"]
            con.commit()
        except requests.exceptions.ConnectionError:
            print "Connection Timed out while scraping:",entry["Title"] ,"site may be down."
        # if auto_up == True:
        #     update_last_read(entry['Title'], cur, con)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit("Please pass '--check' or '--bookmarks' as an argument to check manga.")
    con = sqlite3.connect('mycheckmanga.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if (sys.argv[1]=='--check'):
        cache_dict = {}
        check_manga(cur, con, cache_dict)
        con.close()
    elif (sys.argv[1]== '--bookmarks'):
        cur.execute("SELECT Title, LastChapterRead FROM manga")
        for manga in cur.fetchall():
            print manga 







