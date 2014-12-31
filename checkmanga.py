from bs4 import BeautifulSoup
import requests
import sqlite3

con = sqlite3.connect('manga.db')
cur = con.cursor()
    

def db_get_entry_info(title, cur=cur):
    """Input: Manga title, Output: Returns a tuple of the form: (url, last_chapter_read)"""
    cur.execute("SELECT * FROM manga")
    while True:
        row = cur.fetchone()
        if row == None:
            break
        if row[0] == title:
            return (row[1], row[2])
    return None


def scrape_latest_chapter(title, url=None):
    if url == None:
        url = db_get_entry_info(title, cur)[0]
        if url == None:
            print "Title was not found in database."
            return None
    bsoup = BeautifulSoup(requests.get(url).text)
    latest_chapter = bsoup.find_all('ul',{'class':'chapter_list'})[0].li.a.text[29:]
    #if using mangatown use above, if parsing mangafox use bsoup.body.find_all('a',{'class':'tips'})[0].text
    return latest_chapter
    

def make_db(db_name):
    manga = (('Btooom!','http://mangafox.me/manga/btooom/', '0'), 
        ('Bleach', 'http://mangafox.me/manga/bleach/', '0'), 
        ('Magi - Labyrinth of Magic', 'http://mangafox.me/manga/magi_labyrinth_of_magic/', '0'), 
        ('Magi - Sinbad no Bouken', 'http://mangafox.me/manga/magi_sinbad_no_bouken/', '0'),
        ('The Rising of the Shield Hero', 'http://mangafox.me/manga/tate_no_yuusha_no_nariagari/', '0'), 
        ('Onepunch-man', 'http://mangafox.me/manga/onepunch_man/', '0'),
        ('Mob Psycho 100', 'http://mangafox.me/manga/mob_psycho_100/', '0'),
        ('Attack on Titan', 'http://mangafox.me/manga/shingeki_no_kyojin', '0'),
        ('Attack on Titan: Before the Fall', 'http://mangafox.me/manga/shingeki_no_kyojin_before_the_fall/', '0'), 
        ('Hunter x Hunter','http://mangafox.me/manga/hunter_x_hunter/', '0'))
    con = sqlite3.connect(db_name)
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS manga")
        cur.execute("CREATE TABLE manga(Title TEXT, url TEXT, LastChapter TEXT)")
        cur.executemany("INSERT INTO manga VALUES(?,?,?)", manga)       
    con.close()


def db_add_title(title, url, cur=cur):
    latest_chapter = scrape_latest_chapter(title, url)
    if db_get_entry_info(title) == None:
        cur.execute("INSERT INTO manga VALUES(?,?,?)", (title, url, latest_chapter))
    else:
        cur.execute("UPDATE manga SET url=(?), LastChapter=(?) WHERE Title=(?)", (url, latest_chapter, title))
    con.commit()

def db_delete_title(title, cur=cur):
    cur.execute("DELETE FROM manga WHERE title=(?)", (title,))
    con.commit()

def db_update_entry_info(title, cur=cur, url=None, last_chapter_read=None):
    if url != None:
        cur.execute("UPDATE manga SET url=(?) WHERE title=(?)",(url,title))
    if last_chapter_read != None:
        cur.execute("UPDATE manga SET LastChapter=(?) WHERE title=(?)", (last_chapter_read,title))
    con.commit()

def db_update_all(cur=cur):
    cur.execute("SELECT * FROM manga")
    rows = cur.fetchall()
    for row in rows:
        cur.execute("UPDATE manga SET LastChapter=(?) WHERE title=(?)", (scrape_latest_chapter(row[0], row[1]),row[0]))
    con.commit()

def check_manga(cur=cur):
    cur.execute("SELECT * FROM manga")
    rows = cur.fetchall()
    for row in rows:
        latest_chapter = scrape_latest_chapter(row[0])
        if latest_chapter != row[2]:
            cur.execute("UPDATE manga SET LastChapter=(?) WHERE title=(?)", (scrape_latest_chapter(row[0], row[1]),row[0]))
            print 'A new chapter has been released for ' + row[0] 
            con.commit()
    return None


check_manga()

con.close()

