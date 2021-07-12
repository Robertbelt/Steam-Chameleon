class userInfo:
    email_consent = False
    
    def __init__(self, steam_login, steam_password):
        self.steam_login = steam_login
        self.steam_password = steam_password
    
    def set_email_info(self, imap_server, email_login, email_password):
        self.imap_server = imap_server
        self.email_login = email_login
        self.email_password = email_password
        