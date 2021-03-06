"""
1. Prompt user for a source, destination and departure date - DONE
1a. User may enter an airport code OR text that can be used to find an airport code - DONE
1b. USER MUST SELECT WHICH AIRPORT FROM A LIST OF AIRPORTS
2. Search for source and destination must be case-insensitive - DONE
3. Return all flights with available seats - DONE
4. Include all flights including ones with 1 connection - DONE
5. Result will include -> flightno, src, dst, dep_time, arr_time, number_of_stops, layover time (for non-direct), price and number of seats - DONE
6. Sorted by price (lowest to highest) - DONE
7. User should have ability to sort - DONE
"""

import sys
import cx_Oracle
from creds import user
from creds import password

#get user
#user = input("Username [%s]: " % getpass.getuser())
#if not user:
   # user = getpass.getuser()

#get password
#password = getpass.getpass()
#connection string
connection_string = ''+user+'/'+password+'@gwynne.cs.ualberta.ca:1521/CRS'

#1 - Prompt user for a source, destination and a departure date


try:
    #establish a connection
    first = input("Please enter first letter ")
    second = input("Please enter second letter ")
    connection = cx_Oracle.connect(connection_string)

    #make query
    query = "select sname from c291.students where sname > '%s' and sname < '%s' order by sname" % (first, second)
    #query = "select * from search_flights"
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    connection.close()
except cx_Oracle.DatabaseError as exc:
    error, = exc.args
    if error.code == 955:
        print("Table already exists")
    elif error.code == 1017:
        print("Invalid Credentials")
    else:
        print(sys.stderr, "Oracle code: ", error.code)
        print(sys.stderr, "Oracle message: ", error.message)





