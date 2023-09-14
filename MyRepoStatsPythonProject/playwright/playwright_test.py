from django.contrib.staticfiles.testing import StaticLiveServerTestCase 
from playwright.sync_api import sync_playwright

class MyViewTests(StaticLiveServerTestCase): 
    @classmethod 
    def setUpClass(cls): 
        super().setUpClass() 
        cls.playwright = sync_playwright().start() 
        cls.browser = cls.playwright.chromium.launch() 

    @classmethod 
    def tearDownClass(cls): 
        cls.browser.close() 
        cls.playwright.stop() 
        super().tearDownClass() 

    def test_login(self): 
        page = self.browser.new_page()
        page.goto(f"{self.live_server_url}/")
        assert page.title() == "MyRepoStatsPython"
        page.close()
