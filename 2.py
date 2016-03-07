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
import getpass
from creds import *
import datetime
import random

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
    connection = cx_Oracle.connect(connection_string)
    #make query
    query = "select * from search_flights where flightno1 = 'WJ1172' and stops = 0 and price = 455 and extract(month from dep_date) = 12 and extract(day from dep_date) = 12"
    #query = "select * from search_flights"
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        if row[1] == None:
            print("flight no:", row[0])
            flightno = row[0]
        else:
            print("flight no1:", row[0])
            print("flight no2:", row[1])
        print("src", row[2])
        print("dst", row[3])
        print("dep_date", row[4])
        dep_date = row[4]
        print("dep_time", row[5])
        print("arr_time", row[6])
        print("layover", row[7])
        print("stops", row[8])
        print("fare type", row[9])
        fare = row[9]
        print("seats", row[10])
        print("price", row[11])
        paid_price = row[11]
        cursor.close()
    email = "bashir1@ualberta.ca"
    name = input("Name: ").title()
    query_passenger = "select * from passengers where name = '%s' and email = '%s'" % (name, email)
    cursor_passenger = connection.cursor()
    cursor_passenger.execute(query_passenger)
    rows = cursor_passenger.fetchall()
    if len(rows) > 0:
        for row in rows:
            print(row)
    else:
        print("Passenger not found. Creating a new passenger...")
        country = input("Country of Issue:  ").title()
        name = str(name)
        data = [(email, name, country)]
        insert_connection = connection.cursor()
        insert_connection.bindarraysize = 1
        insert_connection.setinputsizes(20, 20, 10)
        insert = "insert into passengers(email, name, country) values (:1, :2, :3)"
        insert_connection.prepare(insert)
        insert_connection.executemany(None, data)
        connection.commit()
        insert_connection.close()
        print("user created")
    print("creating ticket...")
    #does not check if ticket already exists, but it creates a very large random number
    tno = random.randint(199999999, 999999999)
    data = [(tno, name, email, paid_price)]
    cursor = connection.cursor()
    #cursor.bindarraysize = 1
    #cursor.setinputsizes(int, 20, 20, float)
    insert = "insert into tickets(tno, name, email, paid_price) values(:1, :2, :3, :4)"
    cursor.executemany(insert, data)
    connection.commit()
    print("ticket created...")
    cursor.close()
    print("creating booking...")
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    seat = str(random.randint(1,20))+random.choice(letters)     
    data = [(tno, flightno, fare, dep_date, seat)]
    cursor = connection.cursor()
    insert = "insert into bookings(tno, flightno, fare, dep_date, seat) values (:1, :2, :3, :4, :5)"
    cursor.executemany(insert, data)
    connection.commit()
    cursor.close()
    print("ticket number %d has been created successfully" % (tno))        
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
        




