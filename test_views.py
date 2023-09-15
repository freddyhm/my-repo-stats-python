import os
import django
django.setup()

from django.contrib.staticfiles.testing import StaticLiveServerTestCase 
from playwright.sync_api import sync_playwright

class MyViewTests(StaticLiveServerTestCase): 
    @classmethod 
    def setUpClass(cls):
        os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true" 
        super().setUpClass() 
        cls.playwright = sync_playwright().start() 
        cls.browser = cls.playwright.chromium.launch() 

    @classmethod 
    def tearDownClass(cls): 
        cls.browser.close() 
        cls.playwright.stop() 
        super().tearDownClass() 

    def test_has_title(self): 
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/")
        assert page.title() == "MyRepoStatsPython"
        page.close()

    def test_header_contains_name_of_project(self): 
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/")
        assert page.inner_text('header') == "MyRepoStatsPython"
        page.close()

    def test_body_contains_subtitle(self): 
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/")
        assert "When are commits typically made during the day?" in page.inner_text('body')
        page.close()

    def test_body_contains_morning_entry(self): 
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/")
        assert "Morning:" in page.inner_text('body')
        page.close()

    def test_body_contains_afternoon_entry(self): 
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/")
        assert "Afternoon:" in page.inner_text('body')
        page.close()

    def test_body_contains_evening_entry(self): 
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/")
        assert "Evening:" in page.inner_text('body')
        page.close()

        
