import imaplib
import sys
from time import sleep
import requests
import tempfile
import urllib.request
import email
import os
from PIL import Image
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.remote import webelement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from user import userInfo
from user_manager import UserManager
import pickle


def FindImg(soup):
    targetProfilePictureDiv = soup.find("div", "playerAvatarAutoSizeInner")
    targetImage = targetProfilePictureDiv.find("img")
    imageLink = targetImage.attrs["src"]
    GetImg(imageLink)


def GetImg(imageLink):
    urllib.request.urlretrieve(imageLink, "ProfilePictureCopy")


def get_steam_guard(email_login, email_password):

    IMAP_server = "imap.mail.yahoo.com"
    imap = imaplib.IMAP4_SSL(IMAP_server)

    try:
        status, summary = imap.login(email_login, email_password)
        if status == "OK":
            print(summary)
            imap.select("INBOX")
            type, data = imap.search(None, '(FROM "STEAM SUPPORT")')

            data = str(data[0]).replace("b", "")
            data = data.replace("'", "")
            data = list(map(int, data.split()))

            email_index = str(data[len(data) - 1])
            email_index = email_index.encode()

            res, msg = imap.fetch(email_index, "(RFC822)")
            whole_body = msg[0][1]
            message = email.message_from_string(whole_body.decode("utf-8"))
            if message.is_multipart():
                i = 0
                for payload in message.get_payload():
                    if i == 0:
                        body = payload.get_payload()
                        i += 1
            else:
                print(message.get_payload())

            fd, path = tempfile.mkstemp()
            try:
                with os.fdopen(fd, "w") as tmp:
                    tmp.write(body)

                with open(path, "rb") as f:
                    i = 0
                    for line in f:
                        i += 1
                        if i == 6:
                            steam_guard = line
            finally:
                os.remove(path)

            steam_guard = steam_guard.decode()
            imap.close()
            print(steam_guard)
            return steam_guard

    except imaplib.IMAP4.error:
        print("Error while Logging in to email account")
        imap.close()
        sys.exit(0)


def main_menu(user, user_manager):
    print("1. Copy Profile\n2. Change Setting")
    user_input = int(input("Select An Option: "))
    if user_input == 1:
        copy_profile(user)

    elif user_input == 2:
        print(user_manager.show_user_settings())
        setting_index = int(input("Select Which Setting You Would Like To Change: "))

        while setting_index <= 0 or setting_index > 5:
            setting_index = int(input("Plase Select A Valid Option\n"))

        # Toggle; No input
        if setting_index == 3:
            user_manager.update_setting(user, setting_index, setting_value="")
        else:
            setting_value = input("Enter Your New Value: ")
            user_manager.update_setting(user, setting_index, setting_value)
        
        user_manager.pickle_user(user)
        main_menu(user, user_manager)

    else:
        print("Incorrect Input: Pick a valid choice: ")
        main_menu(user, user_manager)


def copy_profile(user):
    targetURL = input("Please Enter a target URL: ")
    websiteHTML = requests.get(targetURL)
    soup = BeautifulSoup(websiteHTML.text, "html.parser")
    driver = webdriver.Chrome(ChromeDriverManager().install())

    FindImg(soup)
    profileName = soup.find("span", "actual_persona_name").text

    driver.get(
        "https://steamcommunity.com/login/home/?goto=%2Fprofiles%2F76561198031035420%2Fedit%2Finfo"
    )

    wait = WebDriverWait(driver, 1000)
    Steam_account_login = driver.find_element(By.NAME, "username")
    Steam_account_login.send_keys(user.steam_login)

    steam_account_password = driver.find_element(By.ID, "input_password")
    steam_account_password.send_keys(user.steam_password)
    # error_message = driver.find_element(By.ID, "error_display")
    login_button = driver.find_element(By.CLASS_NAME, "login_btn")
    login_button.click()
    steam_guard = get_steam_guard(user.email_login, user.email_password)

    if user.email_consent:
        code_box = driver.find_element(By.ID, "authcode")
        code_box.send_keys(steam_guard)

        name_box = driver.find_element(By.ID, "friendlyname")
        name_box.send_keys("SteamChamelon")
        try:
            submit_button = driver.find_element(By.CLASS_NAME, "auth_button_leftbtn")
            submit_button.click()

        except:
            pass

        # proceed_button = driver.find_element(By.ID, "success_continue_btn")
        proceed_button = wait.until(
            EC.visibility_of_element_located((By.ID, "success_continue_btn"))
        )
        proceed_button.click()

    # driver.get("https://steamcommunity.com/profiles/76561198031035420/edit/info")
    element = wait.until(EC.visibility_of_element_located((By.NAME, "personaName")))

    # nameRequest = requests.post("https://steamcommunity.com/profiles/76561198031035420/edit/", FormData(profileName))

    while True:
        pass


def main():
    user_manager = UserManager()

    try:
        user = user_manager.load_pickled_user()

    except:
        user = user_manager.get_user_info()
        user_manager.pickle_user(user)

    main_menu(user, user_manager)


main()

# r = requests.get("https://steamcommunity.com/id/RawrCapture/")
# soup = BeautifulSoup(r.text, "html.parser")


# imageLink = FindImgURL(soup)
# urllib.request.urlretrieve(imageLink, "gfg.jpg")

# img = Image.open('gfg.jpg')
# img.show()
