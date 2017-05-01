import requests
import sqlite3
import bs4 as bs
import os
from flask import Flask, render_template, make_response, jsonify, g


app = Flask(__name__)

app.config.from_object(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'mycheckmanga.db'),
    SECRET_KEY='development key',
    DEBUG=True,
    #USERNAME='admin',
    #PASSWORD='default'
))

@app.route('/')
def main_page():
    """Returns the main page for the check_manga site."""
    return render_template('main_page.html')

@app.route('/checkmanga/', methods=['POST'])
def check_manga():
    """Connects to the db, looks up all manga marked as 'Ongoing' scrapes all of those titles, returns their status as JSON.
    Input: The cursor object and an auto_update boolean (default=True) that tells the function whether to automatically update LastChapterRead to be the same as MostRecentChapter.
    Output: None. Updates the DB by scraping for chapters for manga where Status = 'Ongoing' and where MostRecentChapter = LastChapterRead"""


@app.route('/addtitle/<title>', methods=['POST'])
def add_title(title):
    """Adds a title to the to-check list in the database."""
    cur = get_db().cursor()
    
    pass

@app.route('/removetitle/<title>')
def remove_title(title):
    """Removes a title from the to-check list in the database."""
    cur = get_db().cursor()

    pass

@app.route('/getmangalist/', methods=['GET'])
def get_manga_list():
    """Gets the to-check list from the database and returns to the user as JSON."""
    cur = get_db().cursor()
    cur.execute("SELECT * FROM manga")
    all_rows = cur.fetchall()

    manga_list = [dict(zip(manga.keys(), manga)) for manga in all_rows]

    return jsonify({"manga": manga_list})


@app.route('/getmangasites/', methods=['GET'])
def get_supported_sites():
    """Gets a list of all the sites that are supported by checkmanga from the database."""
    cur = get_db().cursor()
    cur.execute("SELECT * from sites")
    all_rows = cur.fetchall()

    site_list = [dict(zip(site.keys(), site)) for site in all_rows]

    return jsonify({"sites": site_list})

@app.route('/getmangaforsite/<site>', methods=['GET'])
def get_manga_for_site(site):
    """Gets a list of all the manga titles that are on a particular site from the database."""
    
    pass

@app.teardown_appcontext
def close_db(error):
    """Close the db at end of request"""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def connect_db():
    """Connects to db specificed in config."""
    con = sqlite3.connect(app.config['DATABASE'])
    con.row_factory = sqlite3.Row 
    return con 

def get_db():
    """Open a new db connection if there is not one yet for current app context"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

# @app.cli.command('initdb')
# def initdb_command():
#   """Initializes the db"""
#   init_db()
#   print('Initialized the db')

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

def scrape_latest_cover(url, site_path):
    """Input: A url string and a 'site_path' which is essentially a Json object. (A list of dictionaries. The dictionaries are html tags and are arranged in a specific order.)
    Output: A string scraped from the provided url that is the latest chapter of the manga at that url."""
    cover = BSoup(requests.get(url, timeout=30).text)
    for tag in site_path:
        if tag['TagClass'] != None:
            chapter = cover.find(tag['TagName'], {'class':tag['TagClass']})
        else:
            chapter = cover.find(tag['TagName'])
    return chapter['src']



 