DROP TABLE IF EXISTS manga;
DROP TABLE IF EXISTS sites;
DROP TABLE IF EXISTS tags;
CREATE TABLE sites(
	SiteName TEXT PRIMARY KEY,
);
CREATE TABLE manga(
	Title TEXT PRIMARY KEY,
	Site TEXT,
	Status TEXT,
	Url TEXT,
	LastChapterRead TEXT,
	MostRecentChapter TEXT,
	FOREIGN KEY(Site) REFERENCES sites(SiteName)
);
CREATE TABLE tags(
	ID INT PRIMARY KEY,
	Site TEXT,
	TagName TEXT,
	TagClass TEXT,
	FOREIGN KEY(Site) REFERENCES sites(SiteName)
);


