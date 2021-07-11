## **AutoInsta**
This project is made with the help of Selenium drive and the Python. This project is capable of removing followers and following from your profile and it can even download the media file such as images and videos of the post.

<img src="AutoInsta.png" alt="poster" width="450" height="400">


### What We are going to do?  
<ol>
    <li>Making a Login Script</li>
    <li>Accessing the timeline feeds and downloading the media files</li>
    <li>Managing the followers and followings</li>
    <li>How to run our code</li>
</ol>


### Libraries/Tools required : -  
<ol>
    <li>Chrome webdriver(same version as chrome browser)</li>
    <li>Requests library</li>
    <li>Selenium library</li>
    <li>Urllib3</li>
</ol>


### Installing Libraries/Tools  
**For Chrome Web driver**
You can download it from <a href="https://chromedriver.chromium.org/downloads">here</a>

If you are unable to install then you can follow this link <a href="https://www.youtube.com/watch?v=dz59GsdvUF8">Youtube</a>

**Installing libraries**

```
pip install requests
pip install urllib3
pip install selenium
```


### Before moving ahead, We must be aware of Css selectors  
### What are selectors/locators?  
A **CSS Selector** is a combination of an element selector and a value which identifies the web element within a web page.
**The choice of locator depends largely on your Application Under Test**

**Id**
An element’s id in XPATH is defined using: “[@id='example']” and in CSS using: “#” - ID's must be unique within the DOM.
Examples:

```
XPath: //div[@id='example']
CSS: #example
```

**Element Type**
The previous example showed //div in the xpath. That is the element type, which could be input for a text box or button, img for an image, or "a" for a link. 

```
Xpath: //input or
Css: =input
```

**Direct Child**
HTML pages are structured like XML, with children nested inside of parents. If you can locate, for example, the first link within a div, you can construct a string to reach it. A direct child in XPATH is defined by the use of a “/“, while on CSS, it’s defined using “>”. 
Examples:
```                        
XPath: //div/a
CSS: div > a
```

**Child or Sub-Child**
Writing nested divs can get tiring - and result in code that is brittle. Sometimes you expect the code to change, or want to skip layers. If an element could be inside another or one of its children, it’s defined in XPATH using “//” and in CSS just by a whitespace.
Examples:
```
XPath: //div//a
CSS: div a
```

**Class**
For classes, things are pretty similar in XPATH: “[@class='example']” while in CSS it’s just “.” 
Examples:
```
XPath: //div[@class='example']
CSS: .example
```

### For complex elements, We will use Xpath selectors  
**Xpath** in Selenium is an XML path used for navigation through the HTML structure of the page. It is a syntax or language for finding any element on a web page using XML path expression. XPath can be used for both HTML and XML documents to find the location of any element on a webpage using HTML DOM structure.

**Syntax for XPath selenium:**
XPath contains the path of the element situated at the web page. Standard XPath syntax for creating XPath is.
```Xpath=//tagname[@attribute='value']```
<img class="img-fluid" title="XPath in Selenium: Complete Guide" alt="Basic Format of XPath" src="https://www.guru99.com/images/3-2016/032816_0758_XPathinSele1.png">
<ul>
    <li><strong>// :</strong> Select current node. </li>
    <li><strong>Tagname: </strong>Tagname of the particular node. </li>
    <li><strong>@:</strong> Select attribute. </li>
    <li><strong>Attribute:</strong> Attribute name of the node. </li>
    <li><strong>Value:</strong> Value of the attribute. </li>
</ul>
For More Info. You can visit <a href="https://www.guru99.com/xpath-selenium.html">Here</a>

## Step 1 -> Making a Login Script  
We will make a script which will take the username and password from the config file and login to the user account so that we can perform other activites
First make a **config** file containing username and password.

```
USERNAME = ""
PASSWORD = ""
```

**Writing script**  

First initiate the Chrome webdriver, base path and user url

```
BASE_DIR = os.path.dirname(__file__)
browser = webdriver.Chrome()
user_url = f"https://www.instagram.com/{USERNAME}"
```

**Login Function**  

We will use the css selectors to locating the username field and password field. After entering the username and password at correct places, we click the submit button by location it by <tt>button[type='submit']</tt>

```
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
```

## Step 2 -> Accessing the timeline feeds and downloading the media files  

It will open the user timeline and downloads media files depending upon the input passed.

```
def get_media(username=USERNAME, media_type=None, count=3, browser=browser)
.....
```

It will take 4 keyword argument.
<ol>
      <li><strong>count</strong> It refers to the number of post it should search to download.</li>
      <li><strong>username</strong> Don't pass any username parameter if you want to download the self account post otherwise mention the username of other people.</li>
      <li><strong>media_type</strong> It can be anyone either img or video but you need to pass the parameter in lower case. Don't pass any parameter to download both media  type.</li>
      <li><strong>browser</strong> It is just an instance of web driver</li>
</ol>

```
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
    ...
    ... 
```

It will first fetch the url. Then initiate the base dir for downloading media files.

Then It will call the <tt>getting_all_post</tt> function to retrieve all the media urls.

**<tt>getting_all_post</tt> Function**
It will take two arguments
<ol>
    <li><strong>media_type</strong> It can be anyone either img or video but you need to pass the parameter in lower case. Don't pass any parameter to download both media  type.</li>
    <li><strong>count</strong> It refers to the number of post it should search to download.</li>
</ol>

media nested array is intialized. The **zero index** will contains all the images in the post while the **first** index will contains all the video links

```
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
```

It will get the src url of video and img using the <tt>get_src_from_post</tt> function so that we can download later.

**<tt>get_src_from_post</tt> Function**
It will take the source url from a particular post

```
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
```

Once we get all the urls, we will now download all the media files required.

Continuing with the <tt>get_media</tt> function.

```
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
```

We will now iterate over the list of all media urls.
We will be using the **urlparse** from the **urllib3** library to name our particular media file.

Now we will request that url using the **Requests** library to download it. If the status_code is 200 (or response is ok) then we will write that file in the disk at the preferred location.

## Step 3 -> Managing the followers and followings  
We can follow other suggested users or unfollow the ones that are not following us.

### Following Management  
It will remove a particular no of following
**How does this code works ?**  
<ol>
    <li>Gets the user profile/timeline page</li>
    <li>Open the following section</li>
    <li>Then checks if count of following is greater then 12 then it will scroll and find others following as first page only contains 12 followings</li>
    <li>It will remove following until input no of followings are not removed</li>
</ol>

```
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
    while following_removed &gl; remove:
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
```

It will use a <tt>open_following_section</tt> Function to follow the following section.
**<tt>open_following_section</tt> Function**

```
def open_following_section():
    follow_section_x_path = "//a[contains(@href,'following')]"
    follow_section = browser.find_element_by_xpath(follow_section_x_path)
    follow_section.click()
```

For scrolling bottom , we have used the <tt>scroll_to_bottom</tt> Function using the execute javascript function

```
# it scrolls a particular section of the site
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
```

We have also used the <tt>unfollow_btn</tt> function to click the unfollow button.

```
# finds the unfollow btn and click it.
def unfollow_btn():
un_path = "//button[contains(text(),'Unfollow')]"
un_follow = browser.find_element_by_xpath(un_path)
un_follow.click()
```

Once our task is achieved, we closed that section using the <tt>close_btn</tt>.

```
def close_btn():
    close_btn_path = "//*[name()='svg' and @aria-label='Close']"
    close = browser.find_element_by_xpath(close_btn_path)
    close.click()

```

### Managing Followers  
It will help us to unfollow the users that are not following us
**How does this code works**
<ol>
    <li>Gets the following page</li>
    <li>Then opens the following section</li>
    <li>Gets all the users so that we can compare later with the followers</li>
    <li>Then open the followers page</li>
    <li>Gets all the followers and compare with the following</li>
    <li>Remove the ones which are not following us</li>
</ol>

```
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
```

we have already discussed about the <tt>open_following_section</tt> , <tt>unfollow_btn</tt>, and <tt>close_btn</tt> Function. Lets discuss the other remained function used in this program.

**<tt>open_follower_section</tt> Function**

```
def open_follower_section():
    follow_section_x_path = "//a[contains(@href,'followers')]"
    follow_section = browser.find_element_by_xpath(follow_section_x_path)
    follow_section.click()
```

### Lets merge all the codes together  
```
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
    while following_removed &lt; remove:
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
```  

#### **How to setup :-**
1. First of all, install all the dependencies by `python3 install -r requirements.txt` in the cmd.
2. Then you need to install the selenium web driver in your system. You can follow this link <a href="https://www.youtube.com/watch?v=dz59GsdvUF8">Youtube</a>
3. Now you need to change the username and password in the config.py folder or you can give it on later during the login.
4. There are three features that our project provide :-
    A. **Remove Following anyone**.
    B. **Remove Following that are not your follower**.
    C. **Download Media**.
5. First you need to login to your download. Run the program in interactive shell. If you have already made changes in the config file. Then you can login by simple command:- `login()` or If you have not entered the credentials then you can login by:- `login(username="ENTER YOUR USERNAME", password="ENTER YOUR SECRET KEY")`
7. **(A). Remove follower.**
Command:- 
`remove_following(remove=Enter the no of followers you want to unfollow)`
Sample :- `remove_following(remove=6)`

8. **(B). Remove following that are not your follower.**
Basic syntax :-
`remove_following_not_followers(count=Enter the number of followers to remove)`
Sample code :- `remove_following_not_followers(count=5)`


9. **(C). Download Media.** It can help you to download any media whether IGTV, Video Or Image.
 Basic Syntax :- get_media(username=USERNAME, media_type=img or video, count=3)
Sample :- 
`get_media(username="therock", media_type=img, count=3)`
 or
 `get_media(count=3)`
 It will download all types of media file where : -

    **_count:_** It refers to the number of post it should search to download.

    **_username:_** Don't pass any username parameter if you want to download the self account post otherwise mention the username of other people.

    **_media_type:_** It can be anyone either img or video but you need to pass the parameter in lower case. Don't pass any parameter to download both media  type.

Note: 
1. The download files will be in same directory with the name of the user. The download media files function has a automatic function which will prevent the duplication of the downloaded files.
2. Don't use the opened browser as it will hinder the working of the code.
3. If you find that the download is not working. There might be two reason :-

    - Instagram might have changed the element position or element attribute
    
    * Your internet might be too slow

    * While downloading the media file. If the media file is video then it will take some more time depending on the internet speed.

**All the issues and PR are most welcomed. Please make a branch before committing any changes.**
