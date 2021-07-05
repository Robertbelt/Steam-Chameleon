import pickle
from user import userInfo

class UserManager:
    def pickle_user(self, user):
        with open ("user_data.pkl", 'wb') as output:
            pickle.dump(user, output, -1)

    def load_pickled_user(self):
        with open("user_data.pkl", 'rb') as input:
            user = pickle.load(input)
            return user

    
    def show_user_settings(self):
       
        user = self.load_pickled_user()
        
        return """\n
        1. Steam Username: %s
        2. Steam Password: %s
        3. Email Consent: %s
        4. Email Login: %s
        5. Email Password: %s""" % (user.steam_login, user.steam_password, user.email_consent,
        user.email_login, user.email_password)
    
    def update_setting(self, user, setting_index, setting_value):
        if setting_index == 1:
            user.steam_login = setting_value
       
        elif setting_index == 2:
            user.steam_password  = setting_value
        
        elif setting_index == 3:
            if(user.email_consent):
                user.email_consent = False
            else:
                user.email_consent = True
       
        elif setting_index == 4:
            user.email_login = setting_value
        
        else:
            user.email_password = setting_value
                



    def get_user_info(self):
        steam_login = input("Enter your Steam ID: ")
        steam_pwd = input("Enter your Steam Password: ")
        user = userInfo(steam_login,steam_pwd)
        user_consent = input("Would you like to setup automatic email steam verification?\n"
        "Enter Y or N:\n")
        incorrect_input = True
        while incorrect_input:
            if user_consent.upper() == "Y":
                email_login = input("Please enter your email address: ")
                email_password = input("Please enter your email password: ")
                user.set_email_info(email_login, email_password)
                user.email_consent = True
                incorrect_input = False
            
            elif user_consent.upper() == "N":
                user.email_consent = False
                incorrect_input = False

            else:
                user_consent = input("Incorrect Input: Please enter Y or N:\n")
                incorrect_input = True
        return user