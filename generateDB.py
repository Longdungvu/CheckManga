import sqlite3
import json

def generate_db_from_json(manga_json, sites_json, db_name='mycheckmanga.db'):
    """Input: Takes the names of two json files, one containing manga and the other containing manga hosting websites as input.
    Output: None. Creates a database with three tables out of the contents of the two json file inputs."""
    manga_list = json.load(open(manga_json, 'r'))
    sites_list = json.load(open(sites_json, 'r'))
    con = sqlite3.connect(db_name)
    with con:
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS manga")
        cur.execute("DROP TABLE IF EXISTS sites")
        cur.execute("DROP TABLE IF EXISTS tags")
        cur.execute("CREATE TABLE sites(SiteName TEXT PRIMARY KEY)")
        cur.execute("CREATE TABLE tags(ID INT PRIMARY KEY, Site TEXT, TagName TEXT, TagClass TEXT, FOREIGN KEY(Site) references sites(SiteName))")
        cur.execute("CREATE TABLE manga(Title TEXT PRIMARY KEY, Site TEXT, Status TEXT, Url TEXT, LastChapterRead TEXT, MostRecentChapter TEXT, FOREIGN KEY(Site) references sites(SiteName))")
        for site in sites_list:
            cur.execute("INSERT INTO sites VALUES(?)", ([site['name']]))
            for tag in site["path"]:
                cur.execute("INSERT INTO tags(Site, TagName, TagClass) VALUES(?,?,?)", (site['name'],tag["name"],tag["class"]))
        for manga_title in manga_list:
            cur.execute("INSERT INTO manga VALUES(:title,:site,:status,:url,:lastChapterRead,:mostRecentChapter)", (manga_title))


#myMangaList.json and myMangaSites.json are example json files I have included that indicate how the json should be formatted for this function to work properly.
    
generate_db_from_json('myMangaList.json', 'myMangaSites.json')