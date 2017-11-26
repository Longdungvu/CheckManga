DROP TABLE IF EXISTS manga;
DROP TABLE IF EXISTS sites;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS completed;

CREATE TABLE sites(
	SiteName TEXT PRIMARY KEY,
);
CREATE TABLE manga(
	Title TEXT PRIMARY KEY,
	Site TEXT,
	Status TEXT,
	Url TEXT,
	LastChapterRead TEXT,
	TimeLastUpdated TEXT,
	TimeLastChecked TEXT,
	MostRecentChapter TEXT,
	CoverImageUrl TEXT,
	FOREIGN KEY(Site) REFERENCES sites(SiteName)
);
CREATE TABLE tags(
	ID INT PRIMARY KEY,
	Site TEXT,
	TagName TEXT,
	TagClass TEXT,
	FOREIGN KEY(Site) REFERENCES sites(SiteName)
);
CREATE TABLE completed(
	Title TEXT PRIMARY KEY,
	Rating INT,
	Review TEXT
);


