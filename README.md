<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- ABOUT THE PROJECT -->
## About The Project

Steam Chameleon is a Python tool that automatically copies any Steam profile and edits your Steam profile to perfectly match within seconds. In-game, the profiles appear completely undifferentiated but the name has an extra Unicode character that is only viewable from outside the game to avoid abuse from scammers.

Features:
* Automatic Steam login and authentication by grabbing the authenticator code from the email sent with IMAP.
* Translates HTML code into Steam Markup tags for accurate text formatting.
* Interacts with the file browser for image upload.
* Profile settings are saved for convenience.

### Built With

* [Selenium](https://www.selenium.dev/)
* [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
* [IMAPLib](https://docs.python.org/3/library/imaplib.html)



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* Update PIP
  ```sh
  pip install --upgrade pip
  ```
* On Windows
  ```sh
  python -m pip install --upgrade pip

  ```
   
### Installation

2. Clone the Repo
   ```sh
   git clone https://github.com/Robertbelt/Steam-Chameleon.git
   ```
3. Install PIP Packages
   ```sh
   pip install -r requirements.txt
   ```
4. For Automatic Authentication 

   Your email must be configured to allow third party applications to login via an app password. Currently, only Gmail and Yahoo emails are supported:
   *  [Gmail](https://support.google.com/accounts/answer/185833?hl=en)
   *  [Yahoo](https://help.yahoo.com/kb/generate-separate-password-sln15241.html)




<!-- USAGE EXAMPLES -->
## Usage

![gif](https://media.giphy.com/media/55Wgnq4YhZPLbDlPIj/giphy.gif)


## Final Comparison

![alt text](https://i.ibb.co/rm3P2PW/Profile-Capture-Recovered.png)

<!-- CONTACT -->
## Contact

Roberto Beltran | robertobelt@yahoo.es | [linkedin](https://www.linkedin.com/in/robertobelt/)  
Project Link: [https://github.com/Robertbelt/Steam-Chameleon](https://github.com/Robertbelt/Steam-Chameleon)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [PyAutoGui](https://pyautogui.readthedocs.io/en/latest/#)
* [Pickle](https://docs.python.org/3/library/pickle.html)
* [Requests](https://docs.python-requests.org/en/master/)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
