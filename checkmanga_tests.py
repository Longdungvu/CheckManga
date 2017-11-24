import unittest
import checkmanga
import mock

class TestCheckMangaUtil(unittest.TestCase):
	def SetUp():
		testDB = checkmanga.CheckMangaUtil('mytest.db')
	def TearDown():

class TestUtilityMethods(TestCheckMangaUtil):
	def test_get_entry_info(self):
    	return
    def test_scrape_latest_chapter(self):
    	return
    def test_get_site_path(self):
    	return


class TestGetMethods(TestCheckMangaUtil):
    def test_get_all_ongoing(self):
    	return
    def test_get_all_bookmarked(self):
    	return
    def test_get_supported_sites(self):
    	return


class TestPostMethods(TestCheckMangaUtil):
    def test_change_manga_status(self):
    	return
    def test_delete_manga(self):
    	return
    def test_add_new_site(self):
    	return
    def test_add_new_manga(self):
    	return
    def test_update_last_read(self):
    	return
    def test_check_manga(self):
    	return
