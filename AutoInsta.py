import os
import requests
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urlparse

from config1 import USERNAME, PASSWORD

BASE_DIR = os.path.dirname(__file__)
browser = webdriver.Chrome()
user_url = f"https://www.instagram.com/{USERNAME}"


# login in the instagram account
def login(browser=browser, username=USERNAME, password=PASSWORD):
    browser.get("https://www.instagram.com/")
    time.sleep(2)
    username_field = browser.find_element_by_name("username")
    username_field.send_keys(username)
    password_field = browser.find_element_by_name("password")
    password_field.send_keys(password)
    btn = browser.find_element_by_css_selector("button[type='submit']")
    time.sleep(2)
    btn.click()


# returning src of a particular post
def get_src_from_post(post_type="img"):
    links = []
    file_path = "//div[@role='button']//img[@style]"
    if post_type == "video":
        file_path = "//video[@type='video/mp4']"
    print(post_type)
    files = browser.find_elements_by_xpath(file_path)
    links += [file.get_attribute('src') for file in files]
    return links


# returning src url from all post
def getting_all_post(media_type, count):
    media = [[], []]
    post_xpath = f"//a[contains(@href,'/p/')]"
    post_media = browser.find_elements_by_xpath(post_xpath)
    search_upto = len(post_media)
    if count and count > search_upto:
        print("only", search_upto, "media files alvailable")
        print("downloading---", search_upto, "files only")
        search_upto = count
    elif count:
        search_upto = count
    for post in post_media[0:search_upto]:
        browser.execute_script("arguments[0].click()", post)
        time.sleep(2.5)
        media[0] += get_src_from_post()
        try:
            media[1] += get_src_from_post(post_type="video")
        except NoSuchElementException:
            pass
        close_btn()

    # only returning the video url from all media url
    if media_type == 'video':
        return media[1]
    elif media_type == 'img':
        return media[0]
    else:
        return (media[0] + media[1])


def get_media(username=USERNAME, media_type=None, count=3, browser=browser):
    person_url = f"https://www.instagram.com/{username}/"
    browser.get(person_url)

    # creating user media directory
    src_path = os.path.join(BASE_DIR, f"{username}")
    os.makedirs(src_path, exist_ok=True)

    # getting media links from the function
    media_elements = getting_all_post(media_type, count)
    print(media_elements)
    time.sleep(1.2)

    # looping through the media links
    for element_url in media_elements:
        # parsing the correct file name
        base_url = urlparse(element_url).path
        filename = os.path.basename(base_url)
        print(base_url, "-------", filename)

        # creating the get request to download the media files
        with requests.get(element_url, stream=True) as r:
            if r.status_code not in range(200, 299):
                print("downloading fails, trying next")
            filepath = os.path.join(src_path, f'{username}{filename}')
            if os.path.exists(filepath):
                print("file already exists")
                continue

            # open created file to write as binary
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content():
                    if chunk:
                        f.write(chunk)
            print(element_url)

    print("-----------Done--------")


# removing a particular no of following
def remove_following(remove=0, browser=browser):
    browser.get(user_url)
    time.sleep(1.2)
    open_following_section()
    following_removed = 0
    if remove > 12:
        time.sleep(1.3)
        scroll_to_bottom("((//nav)[3]//following::div)[1]")
        time.sleep(1)
    following_path = "//a[@title]"
    following_sel_list = browser.find_elements_by_xpath(following_path)
    while following_removed < remove:
        try:
            user_name = following_sel_list[following_removed].text
            following_x_path = f"//a[@title='{user_name}']//following::button"
            following_btn = browser.find_element_by_xpath(following_x_path)
            following_btn.click()
            # print("removed----", user_name)
            following_removed += 1
            time.sleep(1.7)
            unfollow_btn()
            # print("un follow", following_removed)
        except:
            break
    else:
        print("successfully removed", following_removed, "followers")
    close_btn()


# finds the unfollow btn and click it.
def unfollow_btn():
    un_path = "//button[contains(text(),'Unfollow')]"
    un_follow = browser.find_element_by_xpath(un_path)
    un_follow.click()


def open_following_section():
    follow_section_x_path = "//a[contains(@href,'following')]"
    follow_section = browser.find_element_by_xpath(follow_section_x_path)
    follow_section.click()


def open_follower_section():
    follow_section_x_path = "//a[contains(@href,'followers')]"
    follow_section = browser.find_element_by_xpath(follow_section_x_path)
    follow_section.click()


def close_btn():
    close_btn_path = "//*[name()='svg' and @aria-label='Close']"
    close = browser.find_element_by_xpath(close_btn_path)
    close.click()


# it scrolls a particlar section of the site
def scroll_to_bottom(scroll_xpath):
    scroll_time = 1.3
    scroll_element = browser.find_element_by_xpath(scroll_xpath)
    last_height = browser.execute_script("return arguments[0].scrollHeight;", scroll_element)
    while True:
        browser.execute_script("arguments[0].scrollTo(0, arguments[1]);", scroll_element, last_height)
        time.sleep(scroll_time)
        new_height = browser.execute_script("return arguments[0].scrollHeight;", scroll_element)
        if new_height == last_height:
            break
        last_height = new_height


# it removes the following that are not your follower
def remove_following_not_followers(count=None, browser=browser):
    browser.get(user_url)
    time.sleep(1.3)
    open_following_section()
    time.sleep(1.3)
    scroll_to_bottom("((//nav)[3]//following::div)[1]")
    time.sleep(1)

    following_path = "//a[@title]"
    following_sel_list = browser.find_elements_by_xpath(following_path)
    following_list = {x.text for x in following_sel_list}
    print("followings are ", len(following_list), "--------------", following_list)

    close_btn()
    time.sleep(1)
    open_follower_section()
    time.sleep(1)
    scroll_to_bottom("((//div[@role='dialog']//div)[1]//div)[5]")

    followers_path = "(((//div[@role='dialog']//div)[1]//div)[5]//ul)[1]//a[@title]"
    followers_sel_list = browser.find_elements_by_xpath(followers_path)
    followers_list = {x.text for x in followers_sel_list}
    close_btn()
    print("followings are ", len(followers_list), "-------------------", followers_list)

    unwanted_follower = following_list - followers_list
    no_of_unwanted_follower = len(unwanted_follower)
    print("length of unwanted follower", no_of_unwanted_follower)
    time.sleep(1)

    open_following_section()
    time.sleep(1)
    scroll_to_bottom("((//nav)[3]//following::div)[1]")

    if count and count > no_of_unwanted_follower:
        print("the count exceeded only", no_of_unwanted_follower, "unwanted followers are there")
        no_of_unwanted_follower = count
    elif count:
        no_of_unwanted_follower = count

    for following in unwanted_follower[0:no_of_unwanted_follower]:
        print("removing---------", following)
        following_x_path = f"//a[@title='{following}']//following::button"
        following_btn = browser.find_element_by_xpath(following_x_path)
        following_btn.click()
    close_btn()

if __name__ == '__main__':
    login(browser)
