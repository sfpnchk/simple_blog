import os
import unittest

from faker import Faker
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

fake = Faker()

USERNAME = "sofiia@gmail.com"
PASSWORD = "sofiiasofiia"
TEST_TITLE = fake.word()
TEST_CONTENT = fake.sentence()
TEST_COMMENT = fake.sentence()


class BlogTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome(f'{os.getcwd()}//chromedriver.exe')
        self.base_url = "http://localhost:8002/"

    def test_blog_scenario(self):
        # Login
        self.browser.get(f'{self.base_url}user/login')
        self.browser.find_element(By.ID, value='hello').send_keys(USERNAME)
        self.browser.find_element(By.ID, value='hi').send_keys(PASSWORD)
        self.browser.find_element(by=By.XPATH, value='/html/body/div/div/div/div/form/button').click()
        self.browser.save_screenshot("Login")

        # Create Post
        self.browser.get(f'{self.base_url}posts/create/')
        WebDriverWait(self.browser, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, "//iframe")))
        self.browser.find_element(by=By.NAME, value='title').send_keys(TEST_TITLE)
        self.browser.find_element(by=By.XPATH, value='body > p').send_keys(TEST_CONTENT)
        self.browser.find_element(by=By.XPATH, value='//form/input[@type="submit"]').click()
        self.browser.save_screenshot("Create Post")

        # See Posts
        self.browser.get(f'{self.base_url}posts/posts')
        self.browser.save_screenshot("See Posts")

        # Add Comment
        self.browser.get(f'{self.base_url}posts/1')
        self.browser.find_element(by=By.ID, value='id_text').send_keys(TEST_COMMENT)
        self.browser.find_element(by=By.XPATH, value='//form/input[@type="submit"]').click()
        self.browser.save_screenshot("Add Comment")


        def tearDown(self):
            self.browser.quit()
