import imaplib
import sys
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


def FindImg(soup):
    targetProfilePictureDiv = soup.find("div", "playerAvatarAutoSizeInner")
    targetImage = targetProfilePictureDiv.find("img")
    imageLink = targetImage.attrs['src']
    GetImg(imageLink)


def GetImg(imageLink):
    urllib.request.urlretrieve(imageLink, "ProfilePictureCopy")


def get_user_info():
    steam_login = input("Enter your Steam ID: ")
    steam_psd = input("Enter your Steam Password")

    user = userInfo(steam_login,steam_psd)

    user_consent = input("Would you like to setup")

def get_logged_on(email_login, email_password):
        
        IMAP_server = "imap.mail.yahoo.com"
        imap = imaplib.IMAP4_SSL(IMAP_server)

        try:
            status, summary = imap.login(email_login, email_password)
            if( status == "OK"):
                print(summary)
                imap.select('INBOX')
                type, data = imap.search(None, '(FROM "STEAM SUPPORT")')
                
                data = str(data[0]).replace("b","")
                data = data.replace("'","")
                data = list(map(int, data.split()))
                
                email_index = str(data[len(data) - 1])
                email_index = email_index.encode()
        
                res, msg = imap.fetch(email_index, "(RFC822)")
                whole_body = msg[0][1]

                message = email.message_from_string(whole_body.decode('utf-8'))
                if message.is_multipart():
                    i = 0
                    for payload in message.get_payload():
                         if i == 0:
                            body = payload.get_payload()
                            i += 1
                else:
                    print (message.get_payload())


                fd, path = tempfile.mkstemp()
                try:
                    with os.fdopen(fd,'w') as tmp:
                        tmp.write(body)

                    with open(path, 'rb') as f:
                        i = 0
                        for line in f:
                            i += 1
                            if i == 6:
                                steam_pass = line
                finally:
                    os.remove(path)
               
                steam_pass = steam_pass.decode()
                print(steam_pass)
                # for response in msg:
                # msg = email.message_from_bytes(msg[-1])
                
                
                # for part in msg.walk():
                #     content_type = part.get_content_type
                #     content_disposition = str(part.get('Content-Disposition'))
                #     body = part.get_payload(decode=True).decode()
              


               









                imap.close()


        except imaplib.IMAP4.error:
            print("Error while Logging in to email account")
            sys.exit(0);




def main():
    # targetURL = input("Please Enter a target URL: ")
    # websiteHTML = requests.get(targetURL)
    # soup = BeautifulSoup(websiteHTML.text, "html.parser")
    # driver = webdriver.Chrome(ChromeDriverManager().install())

    # FindImg(soup)
    # profileName = soup.find('span', 'actual_persona_name').text
    # driver.get("https://steamcommunity.com/profiles/76561198031035420/edit/info")

    # wait = WebDriverWait(driver, 1000)
    # element = wait.until(EC.visibility_of_element_located((By.NAME, 'personaName')))
    
    # element.clear()
    # mailLogin = EmailLogin("Libertad72", "aisforcow3@yahoo.es")
    # element.send_keys(mailLogin.print_email_details())
    
    # while(True):
    #     pass;

    get_logged_on("robertobelt4@yahoo.es", "zaaxkgagbjnbtdsv")

    
    



    # nameRequest = requests.post("https://steamcommunity.com/profiles/76561198031035420/edit/", FormData(profileName))























main()

# r = requests.get("https://steamcommunity.com/id/RawrCapture/")
# soup = BeautifulSoup(r.text, "html.parser")


# imageLink = FindImgURL(soup)
# urllib.request.urlretrieve(imageLink, "gfg.jpg")

# img = Image.open('gfg.jpg')
# img.show()

