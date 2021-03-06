import imaplib, sys, requests, tempfile, email, os, pyautogui, re, threading
from time import sleep
from PIL import Image
from selenium import webdriver
from bs4 import BeautifulSoup
import selenium
from selenium.webdriver.remote import webelement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from user import userInfo
from user_manager import UserManager
from target_user import targetUser
from selenium.webdriver.support.ui import Select

def find_img(soup):
    trgt_profile_pic_div = soup.find("div", "playerAvatarAutoSizeInner")
    target_images = trgt_profile_pic_div.find_all("img")
    urls = [img['src'] for img in target_images] # Finds all the URLs of the images
    
    for url in urls:
        target_image = re.search(r'/([\w_-]+[.](jpg|gif))$', url) # only find .jpg and .gif
    
    return target_image.string

def get_steam_guard(email_login, email_password, imap_server ):

    imap = imaplib.IMAP4_SSL(imap_server)

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
        print("Error while Logging in to email account. Check Login Info")
        imap.close()
        sys.exit(0)

def main_menu(user, user_manager):
    print("1. Copy Profile\n2. Change Setting")
    try:
        user_input = int(input("Select An Option: "))
    except ValueError:
        print("Please Enter a Valid Option")
        main_menu(user, user_manager)

    if user_input == 1:    
        target_url = input("Please Enter a target URL: ")
        login_to_steam(user, target_url)

    elif user_input == 2:
        in_settings_menu = True
        while in_settings_menu:
            print(user_manager.show_user_settings()) # Show Settings
            try:
                setting_index = int(input("Select Which Setting You Would Like To Change: "))
            except ValueError:
                setting_index = -1

            while setting_index <= 0 or setting_index > 7: # Verify Input
                setting_index = int(input("Plase Select A Valid Option: "))

            if setting_index == 3: # Toggle between true and false
                user_manager.update_setting(user, setting_index, setting_value="")

            elif setting_index == 4: # Reselect IMAP
                print("1. Gmail\n2. Yahoo Mail")
                _input = input("Select Your Email Server ")
                loop = True
                while loop:
                    if int(_input) == 1:
                        setting_value = "imap.gmail.com"
                        loop = False
                    elif int(_input) == 2:
                        setting_value = "imap.mail.yahoo.com"
                        loop = False
                    else:
                        _input = input("Invalid Option")
                    
                    user_manager.update_setting(user, setting_index, setting_value)

            elif setting_index == 7: # return to main menu
                in_settings_menu = False
        
            else:
                setting_value = input("Enter Your New Value: ")  # Get the new value
                user_manager.update_setting(user, setting_index, setting_value) # Update in user manager
            
            user_manager.pickle_user(user) # Save user and return to main menu
        main_menu(user, user_manager) 

    else:
        print("Incorrect Input: Pick a valid choice: ")
        main_menu(user, user_manager)

def login_to_steam(user, target_url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
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
    # TODO: listen for a new email instead of sleeping to wait for it to arrive
    sleep(3)
    steam_guard = get_steam_guard(user.email_login, user.email_password, user.imap_server)

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

        proceed_button = wait.until(EC.visibility_of_element_located((By.ID, 
        "success_continue_btn")))
        proceed_button.click()

    # passed steam verification

    edit_profile(wait, driver, target_url)

    while True:
        pass

def find_data(driver, target_url):
    driver_cookies = driver.get_cookies()
    c = {c['name']:c['value'] for c in driver_cookies}
    res = requests.get(target_url, cookies= c)
    soup = BeautifulSoup(res.text,"html.parser")
    
    profile_image_link = find_img(soup)
    profile_username = soup.find("span", "actual_persona_name").text + " ???"


    # Check if there is a real name header visible
    try:
        info_div = soup.find("div", "header_real_name")
        has_name_header =  True
    except:
        has_name_header = False
        print("Failed to find Real Name and country")


    if has_name_header: # Found Name or location info
        try:
            info_div = soup.find("div", "header_real_name")
            profile_real_name = info_div.find("bdi").text
        
            if profile_real_name == '':
                profile_real_name = None
        except:
            print("Real Name not found")

        try:
            info_div_data = info_div.text
            info_div_data = info_div_data.replace('\n', "")
            info_div_data = info_div_data.replace('\r', "")
            info_div_data = info_div_data.replace("\t", "")
            info_div_data = info_div_data.replace("\xa0","")
            if profile_real_name is not None:
                info_div_data = info_div_data.replace(profile_real_name, "")
            
            location_data = info_div_data.split(',')
            
            if(location_data[0] == '' and len(location_data) == 1): # L
                location_data == None
                profile_country = None
                profile_state = None
                profile_city = None
                print("Location data not found")
            else:
                profile_state = None
                profile_city = None
                for i in range(0, len(location_data)):
                    if(location_data[i][0]) == ' ':
                        data  = location_data[i]
                        data = data[:0] + data[1:]
                        location_data[i] = data
        
                
                if len(location_data) == 1:
                    profile_country = location_data[0]
                elif len(location_data) == 2:
                    profile_country = location_data[1]
                    profile_state = location_data[0]
                else:
                    profile_country = location_data[2]
                    profile_state = location_data[1]
                    profile_city = location_data[0]
        except:
            print("Profile Name/Country not found")
            profile_real_name = None
            profile_country = None
            profile_city = None
            profile_state = None
        try:
            profile_description = soup.find("div", "profile_summary")
            profile_description_text = profile_description.text
            profile_description_text = ' '.join(profile_description_text.split())

            children_div = profile_description.find_all("div", "bb_h1")
            for child in children_div:
                child_text = ' '.join(child.text.split())
                child_edited = "[h1]%s[/h1]" % (child_text)
                profile_description_text = profile_description_text.replace(child_text, child_edited)

            children_i = profile_description.find_all("i")
            for child in children_i:
                child_text = ' '.join(child.text.split())
                child_edited = "[i]%s[/i]" % (child_text)
                profile_description_text = profile_description_text.replace(child_text, child_edited)
                
            children_b = profile_description.find_all("b")
            for child in children_b:
                child_text = ' '.join(child.text.split())
                child_edited = "[b]%s[/b]" % (child_text)
                profile_description_text = profile_description_text.replace(child_text, child_edited)

            children_spoiler = profile_description.find_all("span", "bb_spoiler")
            for child in children_spoiler:
                child_text = ' '.join(child.text.split())
                child_edited = "[spoiler]%s[/spoiler]" % (child_text)
                profile_description_text = profile_description_text.replace(child_text, child_edited)

            children_a = profile_description.find_all('a', 'bb_link')
            for child in children_a:   
                try:
                    child_ = child.contents[0].attrs
                except:
                    if 'https://' in child.text or 'http://' in child.text:
                        pass
                    else:
                        name_to_remove = child.get('href').replace("https://steamcommunity.com/linkfilter/?url=https://", '')
                        url = child.get('href').replace("https://steamcommunity.com/linkfilter/?url=", '')
                        name_to_remove = name_to_remove.split('/', 1)[0]
                        name_to_remove = '[%s]' % name_to_remove
                        profile_description_text = profile_description_text.replace(name_to_remove, '')
                        child_text = ' '.join(child.text.split())
                        child_edited = "[url=%s]%s[/url]" % (url, child_text)
                        profile_description_text = profile_description_text.replace(child_text, child_edited)
        except:
            print("Profile Description not found")
            profile_description_text = None

        target_user = targetUser(profile_image_link, profile_username, profile_real_name,
                                profile_country, profile_state, profile_city, profile_description_text)       
        return target_user

def edit_profile(wait, driver, target_url):

    target_user = find_data(driver, target_url)

    # Type target username out
    profile_username_box = wait.until(EC.visibility_of_element_located((By.NAME, "personaName")))
    driver.find_element(By.NAME, "personaName").clear()
    profile_username_box.send_keys(target_user.profile_username)

    # Type Real Name
    profile_name_box = driver.find_element(By.NAME, 'real_name')
    profile_name_box.clear()
    if(target_user.profile_name is not None):
        profile_name_box.send_keys(target_user.profile_name)

    # Type summary
    profile_summary_box =  driver.find_element(By.NAME, 'summary')
    profile_summary_box.clear()
    if target_user.summary is not None:
        profile_summary_box.send_keys(target_user.summary)
    # Go through location tabs
    try: 
        for index in range(0,3):
            location_tabs = driver.find_elements(By.CLASS_NAME, 'DialogDropDown')
            dropdown = location_tabs[index]
            if index == 0 and target_user.profile_country is not None:
                dropdown_option = "//div[@class='dropdown_DialogDropDownMenu_Item_2oAiZ' and text()='%s']" % (target_user.profile_country)
            elif index == 0 and target_user.profile_country is None:
                dropdown_option = "//div[@class='dropdown_DialogDropDownMenu_Item_2oAiZ' and text()='(Do not display)']"
            else:
                if index == 1 and target_user.profile_state is not None:
                    dropdown_option = "//div[@class='dropdown_DialogDropDownMenu_Item_2oAiZ' and text()='%s']" % (target_user.profile_state)
                elif index == 2 and target_user.profile_city is not None:
                    dropdown_option = "//div[@class='dropdown_DialogDropDownMenu_Item_2oAiZ' and text()='%s']" % (target_user.profile_city)
                else:
                    break
            dropdown.click()
            dropdown_select= wait.until(EC.visibility_of_all_elements_located((By.XPATH, dropdown_option)))
            dropdown_select[0].click() # Click on dropdown corresponding to location
    except:
        pass

    
    save_button = driver.find_element(By.CLASS_NAME, 'Primary')
    save_button.click() # Click Save button

    Avatar_button = driver.find_element(By.XPATH, ("//*[contains(text(), 'Avatar')]"))
    Avatar_button.click() # Click on Avatar tab

    upload_button = driver.find_element(By.CLASS_NAME, "DialogButton")
    upload_button.click()
    sleep(1)
    thread = threading.Thread(pyautogui.write(target_user.profile_image))
    thread.start()
    thread.join()
    pyautogui.press('enter') 
    sleep(1.5)
    save_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[text()='Save']")))
    save_button.click()

def main():
    user_manager = UserManager()

    try:
        user = user_manager.load_pickled_user()

    except:
        user = user_manager.get_user_info()
        user_manager.pickle_user(user)

    main_menu(user, user_manager)

main()