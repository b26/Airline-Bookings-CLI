import sys
import cx_Oracle
import getpass
from app import App
#get user
user = input("Username [%s]: " % getpass.getuser())
if not user:
    user = getpass.getuser()

#get password
password = getpass.getpass()
#creates a connection string
connection_string = ''+user+'/'+password+'@gwynne.cs.ualberta.ca:1521/CRS'

#attempts to connect
try:
    connection = cx_Oracle.connect(connection_string)
    #initalize App
    app = App()
    #Start the application and pass in connection
    app.start(connection)
    #Any time the app exists, the connection automatically closes
    connection.close()
except cx_Oracle.DatabaseError as exc:
    #Anytime there's an error in App it exists and enter here.
    error, = exc.args
    if error.code == 955:
        print("Table already exists")
    elif error.code == 1017:
        print("Invalid Credentials")
    else:
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)





