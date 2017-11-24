from bs4 import BeautifulSoup as BSoup
import requests
import sqlite3
import sys
import datetime
#'mycheckmanga.db' is the name of the exmaple database included with this code.

class CheckMangaUtil:
    def __init__(self, db_name):
        """Connects to DB, generates cache for site paths, and generates cursor object."""
        self.con = sqlite3.connect(db_name)        
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.site_path_cache= {}
    def get_entry_info(self, title):
        """Input: Manga title
        Output: Returns a dictionary of the manga's info from the db, keys to the dict are columns of the db."""
        self.cur.execute("SELECT * FROM manga WHERE Title = (?)", [title])
        entry = self.cur.fetchone()
        return dict(entry)
    def scrape_latest_chapter(self, url, site_path):
        """Input: A url string and a 'site_path' which is essentially a Json object. (A list of dictionaries. The dictionaries are html tags and are arranged in a specific order.)
        Output: A string scraped from the provided url that is the latest chapter of the manga at that url."""
        chapter = BSoup(requests.get(url, timeout=30).text, "html.parser")
        for tag in site_path:
            if tag['TagClass'] != None:
                chapter = chapter.find(tag['TagName'], {'class':tag['TagClass']})
            else:
                chapter = chapter.find(tag['TagName'])
        return chapter.text.strip()
    def get_site_path(self, site):
        """Input: The name of a specific manga site
        Output: A list of dictionary-like objects that represent instructions on how to scrape a particular manga site."""
        if self.site_path_cache.get(site) != None:
            site_path = self.site_path_cache.get(site)
        else:
            #The SQL statement below retrieves the "site_path" (aka instructions on how to scrape that manga site) from the tags table of the db.
            self.cur.execute("SELECT * FROM tags WHERE site=(?) ORDER BY ID ASC", [site])
            site_path = self.cur.fetchall()
            self.site_path_cache[site] = site_path
        return site_path 
    def get_all_ongoing(self):
        """Input: None
        Output: Returns a list of all entries in the CheckManga DB manga table where status = 'Ongoing'."""
        self.cur.execute("SELECT * FROM manga WHERE Status = 'Ongoing'")
        all_ongoing = self.cur.fetchall()
        return all_ongoing
    def get_all_bookmarked(self):
        """Input: None
        Output: Returns a list of all entries in the CheckManga DB manga table where status = 'Bookmarked'."""
        self.cur.execute("SELECT * FROM manga WHERE Status = 'Bookmarked'")
        all_bookmarked = self.cur.fetchall()
        return all_bookmarked
    def get_supported_sites(self):
        """Input: None
        Output: Returns a list of all entries in the CheckManga DB sites table."""
        self.cur.execute("SELECT * FROM sites")
        all_sites = [x[0] for x in self.cur.fetchall()]
        return all_sites
    def change_manga_status(self, req):
        """Input: A dictionary object representing request Json.
        Output: Returns success message after changing "status" column of a given entry."""
        self.cur.execute("UPDATE manga SET Status=(?) WHERE Title=(?)", [req["Status"], req["Title"]])
        self.con.commit()
        return {"Success": "Successfully updated manga {0} status to {1}".format(req["Title"],req["Status"])}
    def delete_manga(self, req):
        """Input: A dictionary object representing request Json.
        Output: Returns success message after deleting a title from the manga table of the DB."""
        self.cur.execute("DELETE from manga WHERE Title=(?)", [req["Title"]])
        self.con.commit()
        return {"Success": "Successfully deleted {0} from CheckManga DB".format(req["Title"])}
    def add_new_site(self, req):
        """Input: A dictionary object representing request Json.
        Output: Returns success message after adding a new site to the Sites table of the DB and adding the ordered tags in SitePath as a series of entries into the tags table."""
        self.cur.execute("INSERT into sites VALUES(?)", [req["SiteName"]])
        for i, tag in enumerate(req["SitePath"]):
            self.cur.execute("INSERT into tags VALUES(?,?,?,?)", [i, req["SiteName"], tag["TagName"], tag["TagClass"]])
        self.con.commit()
        return {"Success": "Successfully added site {0} to CheckManga DB".format(req["SiteName"])}
    def add_new_manga(self, req):
        """Input: A dictionary object representing request Json.
        Output: Returns success message after adding new manga title to the manga table."""
        if req["Site"] not in self.get_supported_sites():
            return {"Error": "Requested site currently not supported by checkmanga."}
        MostRecentChapter = self.scrape_latest_chapter(req["Url"], self.get_site_path(req["Site"]))
        LastChapterRead = MostRecentChapter
        TimeLastChecked = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        TimeLastUpdated = TimeLastChecked
        self.cur.execute("INSERT into manga VALUES(?,?,?,?,?,?,?,?,?)", \
            [req["Title"], req["Site"], req["Status"], req["Url"], LastChapterRead, TimeLastUpdated, TimeLastChecked, MostRecentChapter, req["CoverImageUrl"]])
        self.con.commit()
        return {"Success": "Successfully added {0} to CheckManga DB".format(req["Title"])}
    def update_last_read(self, req):
        """Input: A dictionary object representing request Json.
        Output: Returns success message after updating the LastChapterRead of a title in the manga table."""
        self.cur.execute("UPDATE manga SET LastChapterRead = (?) WHERE Title = (?)", [req["LastChapterRead"],req["Title"]])
        self.con.commit()
        return {"Success": "Successfully updated Last Chapter Read of {0} to {1}".format([req["Title"],req["LastChapterRead"]])}
    def check_manga(self):
        """Input: None
        Output:  A JSON object detailing which manga have been updated and which have been not."""
        all_rows = self.get_all_ongoing()
        checkMangaJson = {}  
        for entry in all_rows:
            site_path = self.get_site_path(entry["Site"])
            print "Currently Scraping:", entry["Title"]
            try:
                most_recent_chapter = self.scrape_latest_chapter(entry['Url'], site_path)
                time_last_checked = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
                if entry['MostRecentChapter'] != most_recent_chapter:     
                    self.cur.execute("UPDATE manga SET MostRecentChapter = (?), LastChapterRead = (?), TimeLastUpdated = (?), TimeLastChecked = (?) WHERE Title = (?)", (most_recent_chapter, most_recent_chapter, time_last_checked, time_last_checked, entry["Title"])) 
                    print 'A new chapter has been released for ' + entry["Title"]
                    checkMangaJson[entry["Title"]] = "A new chapter has been released"
                    self.con.commit()
                else:
                    self.cur.execute("UPDATE manga SET TimeLastChecked = (?) WHERE Title = (?)", (time_last_checked, entry["Title"])) 
                    checkMangaJson[entry["Title"]] = "No new chapters have been released since: {0}".format(entry["TimeLastUpdated"])
            except requests.exceptions.ConnectionError:                
                print "Connection Timed out while scraping:",entry["Title"] ,"site may be down."
                checkMangaJson[entry["Title"]] = "Connection Timed out while scraping: {0} site may be down.".format(entry["Title"])
        return checkMangaJson




