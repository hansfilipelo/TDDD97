#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import time

class TwidderTester:

    def __init__(self, host, port, path):
        self.__timeout_time = 1

        self.__email = "email"
        self.__firstname = "firstname"
        self.__lastname = "lastname"
        self.__password = "password"
        self.__city = "city"
        self.__country = "country"
        self.__gender = "gender"
        self.__repeat_password = "repeat-password"
        self.__gender = "gender"

        self.available_fields = [self.__email, self.__firstname, self.__lastname, self.__password, self.__city, self.__country, self.__repeat_password, self.__gender]

        self.twidder_location = host + ":" + port + path
        self.__driver = webdriver.Firefox()
        self.__driver.get(self.twidder_location)

    # -----------------------------
    def sign_up(self, in_email, in_password, in_firstname, in_lastname, in_city, in_country, in_gender):
        sign_up_prefix = "signup-"
        sign_up_fields = {}

        assert in_gender in ["Male", "Female"]

        for field in self.available_fields:
            sign_up_fields[field] = self.__driver.find_element_by_id(sign_up_prefix+field)

        # Fill out form
        sign_up_fields[self.__email].send_keys(in_email)
        sign_up_fields[self.__password].send_keys(in_password)
        sign_up_fields[self.__repeat_password].send_keys(in_password)
        sign_up_fields[self.__firstname].send_keys(in_firstname)
        sign_up_fields[self.__lastname].send_keys(in_lastname)
        sign_up_fields[self.__city].send_keys(in_city)
        sign_up_fields[self.__country].send_keys(in_country)
        Select(sign_up_fields[self.__gender]).select_by_visible_text(in_gender)

        self.__driver.find_element_by_id(sign_up_prefix + "submit").click()

        time.sleep(self.__timeout_time)

        # Assert Sign up OK! is on page
        assert "Sign up OK!" in self.__driver.page_source

        # Clear field so they can be used again
        for key in sign_up_fields.keys():
            if key != self.__gender:
                sign_up_fields[key].clear()

    # -----------------------------

    def sign_in(self, in_email, in_password):
        sign_in_prefix = ""

        # Find fields
        email_field = self.__driver.find_element_by_id(sign_in_prefix+self.__email)
        password_field = self.__driver.find_element_by_id(sign_in_prefix+self.__password)

        # Fill out form
        email_field.send_keys(in_email)
        password_field.send_keys(in_password)
        # Submit
        self.__driver.find_element_by_id(sign_in_prefix+"submit").click()

        time.sleep(self.__timeout_time)

        assert in_email in self.__driver.page_source

    # -----------------------------

    def browse_user(self, username):
        # Browse tab "is not visible" according to selenium, make it visible by javascript
        self.__driver.execute_script("document.getElementById('browse').checked = true;")
        self.__driver.execute_script("document.getElementById('home').checked = false;")
        time.sleep(self.__timeout_time)

        # Fill out form
        browse_form = self.__driver.find_element_by_id("browse-username-form")
        submit_button = self.__driver.find_element_by_id("browse-submit")

        browse_form.send_keys(username)
        submit_button.click()

        time.sleep(self.__timeout_time)

        browse_form.clear()

        assert username in self.__driver.page_source

    # -----------------------------

    def write_post(self, message):
        post_form = self.__driver.find_element_by_id("browse-write-post")
        submit_button = self.__driver.find_element_by_id("browse-write-post-submit")

        post_form.send_keys(message)
        submit_button.click()

        time.sleep(self.__timeout_time)

        post_form.clear()

        assert message in self.__driver.page_source


    def tearDown(self):
        self.__driver.close()
