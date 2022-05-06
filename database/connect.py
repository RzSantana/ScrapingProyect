import mysql.connector

try:
    connexion = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',
        password='',
        db='testScraping'
    )

    if connexion.is_connected():
        print('Connexion from Database: OK')

except Exception as ex:
    print('Failed to connect')
    print(ex)

# Function for close connexion
def connexionClose():
        connexion.close()
        print('Connexion from Database: OFF')

# Function for execute sql code
def executeSQL(self):
    query = connexion.cursor()
    query.execute(self)

def commitSQL():
    connexion.commit()


# # Function for connect from server
# def connexionSV(self):
#     try:
#         self.connexion = mysql.connector.connect(
#             host='localhost',
#             port='3306',
#             user='root',
#             password='',
#         )
#
#         if self.connexion.is_connected():
#             print('Connexion from Server: OK')
#
#     except Exception as ex:
#         print('Failed to connect')
#         print(ex)
#
#     return self.connexion
#
# # Function for execute sql code
# def executeSQL(self):
#     exe = connexionSV().cursor()
#     exe.execute(self)
#
# # Function for check if exist the Database
# def checkDB():
#     nameDB = input('Database name where you want save the datas: ')
#     executeSQL('CREATE DATABASE IF NOT EXISTS {}'.format(nameDB))
#     print('Your select Database is: ' + nameDB)
#
# # Function for connect from database in server
# def connexionDB():
#     try:
#         connexion = mysql.connector.connect(
#             host='localhost',
#             port='3306',
#             user='root',
#             password='',
#             db=checkDB()
#         )
#
#         if connexion.is_connected():
#             print('Connexion from Database: OK')
#
#     except Exception as ex:
#         print('Failed to connect')
#         print(ex)
#
# # Function for close connexion
# def connexionClose():
#     if connexionSV().is_connected():
#         connexionSV().close()
#         print('Connexion from Server: OFF')
