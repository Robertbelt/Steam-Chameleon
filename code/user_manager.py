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

    
    def user_settings(self):
       
        user = self.load_pickled_user()
        
        return """\n
        1. Steam Username: %s
        2. Steam Password: %s
        3. Email Consent: %s
        4. Email Login: %s
        5. Email Password: %s""" % (user.steam_login, user.steam_password, user.email_consent,
        user.email_login, user.email_password)
        