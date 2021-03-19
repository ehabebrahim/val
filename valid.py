from tinydb import TinyDB, Query  # tiny database inheritace
import re  # regix lib for mail validation
from sechashuli import make_pw_hash, \
    check_pw_hash  # hashing class to convert plain password to sha-256 hasing and compare
import datetime

db = TinyDB('usrdb.json')  # defind database location as json file
users = Query()  # implementing data as user query


class validation:  # validation class to check existence and data validity

    def __init__(self, email, username, phone):
        self.email = email
        self.username = username
        self.phone = phone

    def check_existence(self):  # check existence of mail, username and phone data
        status = False
        error = ""
        if db.search(users.email == self.email):  # checking mail
            error = "Email Registered Before"
        elif db.search(users.username == self.username):  # checking username
            error = "User Name is Taken"
        elif db.search(users.phone == self.phone):
            error += "This Phone Number is Used "
        else:
            status = True
            error = "everything is okay "
        return status, error

    def check_validity(self):  # mail Checking validity with regex
        val_status = False
        val_error = ""
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if re.search(regex, self.email):
            val_status = True
        # print("Valid Email")

        else:
            val_error = "Invalid Email"
        #  print("Invalid Email")
        return val_status, val_error


class user:  # main user class for all user data assiging as user or admin

    def __init__(self, first_name, last_name, email, phone, username, role, password, level="normal", score=0):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.username = username
        self.role = role
        self.level = level
        self.score = score
        self.pw_hash = make_pw_hash(password)
        self.rdate = str(datetime.datetime.today().replace(second=0, microsecond=0))

    def adduser(self):  # add user and admin in database
        checker = validation(self.email, self.username, self.phone)
        status, error = checker.check_existence()
        val_status, val_error = checker.check_validity()
        if val_status:
            if not status:
                return True, error
            else:

                db.insert(
                    {'first_name': self.first_name, 'last_name': self.last_name, 'email': self.email,
                     'phone': self.phone,
                     'username': self.username, 'level': self.level,
                     'score': self.score, 'rdate': self.rdate,
                     'password': self.pw_hash, 'role': self.role})
                return True, "Success Sign up"
        else:
            return False, val_error

    def find(key, value):  # find whole data about user/admin using key of search and value

        result = ""
        if key == "username" or key == "phone" or key == "email" or key == "role":
            if key == "username":
                result = db.search(users.username == value)
            elif key == "phone":
                result = db.search(users.phone == value)
            elif key == "email":
                result = db.search(users.email == value)
            elif key == "role":
                result = db.search(users.role == value)
        else:
            result = "invalid search Key"
        if result == []:
            result = "there is no data "
        return result

    def modify(key, pramter, value):  # modifiy user/admin data using key, paramter and value
        if pramter != "password":
            db.update({pramter: value}, users.username == key)

        else:
            print('You gonna to change user password ')
            old_pass = input('Please enter old password\n')
            data = db.get(Query()['username'] == key)
            if check_pw_hash(old_pass, data.get('password')):  # checking password hash to make verifiy changes
                db.update({pramter: value}, users.username == key)
                print("password changed")
            else:
                print("old password is wrong ")

    def delete(key):

        print("You gonna to delete user ")  # "GOD Mode TUTU2020"
        data = db.get(Query()['username'] == key)
        old_pass = input("Please enter password to delete account\n")

        if check_pw_hash(old_pass, data.get('password')):  # checking password hash to make verifiy changes
            db.remove(users.username == key)
            print("account Deleted")
        else:
            print("you Entered wrong password")

class Hall_of_Fame:
    """Class that determines the top 10 users."""

    def __init__(self):
        self.score = 0
        
    def fame(self):

        db = TinyDB('usrdb.json')  
        users = Query() 
        gold_users = db.search(users.level == "Gold")  # A top 10 user must be Gold
        top_ten = []
        gold_users.sort(key=lambda x: x['score'], reverse=True)  # Sorting the users based on scores
        first_ten = list(gold_users)[:10]  # Returning 10 users with highest scores
        #print(self.first_ten)

        if first_ten:
            # print("The top users are: ")
            for i in range(len(first_ten)):
                #return first_ten[i]["username"], first_ten[i]["score"]
                top_ten.append({"username": first_ten[i]["username"], "score": first_ten[i]["score"]})
            return  top_ten
        else:
            return []

