from csv import reader
import pymysql
import json
import string
import random

def password_generator(size=8, number_special=1, number_digit=1):

  # Password must have 8 character at least.
  if size<8:
    size=8

  # at least 1 digit, 1 specical character.  
  if number_digit<1:
    number_digit=1

  if number_special<1:
    number_special=1

  number_ascii_letters = size - number_special - number_digit
  if number_ascii_letters<0:
    number_ascii_letters=1

  password = []
  for _ in range(number_ascii_letters):
    password.append(random.choice(string.ascii_letters))
  for _ in range(number_special):
    password.append(random.choice("_" + "-" + "%") )
  for _ in range(number_digit):
    password.append(random.choice(string.digits) )
  
  random.shuffle(password)

  return ''.join(password)

def create_user(path="userList", version=8):
  createdUsers = {}
  try:
    with open(path,"r") as f:
        users = reader(f)
        
        with connection.cursor() as cursor:
          for user in users:
            username = ''.join(user)
            if username not in createdUsers:            
              try:
                password = password_generator(size=16)
                if version == 8:
                  sql_cu = "CREATE USER IF NOT EXISTS '" + username + "'@'%' IDENTIFIED BY '" + password + "';"
                else:
                  # Syntax for very old MySQL/Mariadb version ( <= MySQL 5.5, <= Mariadb 10.1)
                  sql_cu = "CREATE USER '" + username + "'@'%' IDENTIFIED BY '" + password + "';"
                cursor.execute(sql_cu)
                createdUsers[username] = password
              except pymysql.err.OperationalError as e:
                print(e)
                            
  finally:
    output_json = json.dumps(createdUsers)
    print(output_json)
    print("---Done created users---")

def change_password(path="userList", version=8):
  changedUsers = {}
  try:
    with open(path,"r") as f:
        users = reader(f)
        
        with connection.cursor() as cursor:
          for user in users:
            username = ''.join(user)
            if username not in changedUsers:            
              try:
                password = password_generator(size=16)
                if version == 8:
                  sql_cp = "ALTER USER IF EXISTS '" + username + "'@'%' IDENTIFIED BY '" + password + "';"
                else:
                  # Syntax for very old MySQL/Mariadb version ( <= MySQL 5.5, <= Mariadb 10.1)
                  sql_cp = "SET PASSWORD FOR '" + username + "'@'%' = PASSWORD('" + password + "');"
                cursor.execute(sql_cp)
                changedUsers[username] = password
              except pymysql.err.OperationalError as e:
                print(e)
                         
  finally:
    output_json = json.dumps(changedUsers)
    print(output_json)
    print("---Done update user's password---")


def grant_Privileges(path="priv_list",create_db=False):
  try:
    # CSV file:
    # username, database
    with open(path,"r") as f:
      users = reader(f,delimiter=',')
      with connection.cursor() as cursor:
        for user in users:
          username = ''.join(user[0])
          database = ''.join(user[1])
          
          if create_db:
            try: 
              sql_cd = "CREATE DATABASE `" + database + "` ;"
              cursor.execute(sql_cd)
            except pymysql.err.ProgrammingError as e:
              print(e)

          try:
            sql_grant = """GRANT ALL PRIVILEGES ON `{0}`.* TO `{1}`@`%`;""".format(database,username)
            cursor.execute(sql_grant)
            print("Granted user: {} all privileges on {} ".format(username, database))
          except pymysql.err.OperationalError as e:
            print(e)
        
  finally:
    print("Done grant privileges")
    
# Mariadb 5.
connection = pymysql.connect(read_default_file='.my.cnf',
                              cursorclass=pymysql.cursors.DictCursor)

create_user("userList",version=5)
change_password("userList",version=5)
grant_Privileges("privList.csv")

connection.close()
