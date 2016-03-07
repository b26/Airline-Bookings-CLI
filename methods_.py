import random
import time
import os
import datetime
def search(connection, choosen_flight):
    src = input("Source: ")
    dst = input("Destination: ")
    year = input("Year: ")
    month = input("Month: ")
    day = input("Day: ")
    sortby = input("Sort by number of stops (yes or no)?: ")
    if sortby == 'y' or sortby == 'yes':
        sortby = 'stops, price'
    else:
        sortby = 'price'

    print("Searching for flights on %s/%s/%s..." %  (year, month, day))
    if len(dst) > 3:
        dst = dst.title()
        query_dst = "select acode from airports where city like '%"+dst+"%'"
        cursor_dst = connection.cursor()
        cursor_dst.execute(query_dst)
        rows = cursor_dst.fetchall()
        if len(rows) > 0:
            for i in range(0, len(rows)):
                print(i, rows[i])
                choice = input("Please select which airport ")
                if choice.isdigit():
                    dst = rows[int(choice)][0]
                else:
                    print("invalid choice. choosing the first airport.")
                    dst = rows[0][0]
        else:
            print("Unable to find destinatino airport...")
        cursor_dst.close()
    if len(src) > 3:
        src = src.title()
        query_src = "select acode from airports where city like '%"+src+"%'"
        cursor_src = connection.cursor()
        cursor_src.execute(query_src)
        rows = cursor_src.fetchall()
        if len(rows) > 0:
            for i in range(0, len(rows)):
                print(i, rows[i])
                choice = input("Please select which airport ")
                if choice.isdigit():
                   src = rows[int(choice)][0]
                else:
                    print("invalid choice. choosing the first airport.")
                    src = rows[0][0]
        else:
            print("Unable to find source airport...")
        cursor_src.close()
    src = src.upper()
    dst = dst.upper()
    select = "flightno1, flightno2, src, dst, dep_time, arr_time, layover, stops, fare, seats, price"
    query = "select * from search_flights where src = '%s' and dst = '%s' and extract(month from dep_date)='%s' and extract(day from dep_date) = '%s' and extract (year from dep_date) = '%s' order by %s" % (src, dst, month, day, year, sortby)
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    if len(rows) > 0:
        for i in range(0, len(rows)):
            print(i, rows[i])
    else:
        print("Unable to find flights...")
    booking = input("choose flight or return to the main (return) ")
    print(booking)
    if booking == "return" or booking == "r" and not booking.isdigit():
        pass
    else:
        flight = int(booking)
        choosen_flight.append(rows[flight])

def passenger(connection, name, email):
    query_passenger = "select * from passengers where name = '%s' and email = '%s'" % (name, email)
    cursor_passenger = connection.cursor()
    cursor_passenger.execute(query_passenger)
    rows = cursor_passenger.fetchall()
    if len(rows) > 0:
        print("passenger exists")
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
        print("passenger created")

def ticket(connection, tno, name, email, paid_price):
    print("creating ticket...")
    data = [(tno, name, email, paid_price)]
    cursor = connection.cursor()
    insert = "insert into tickets(tno, name, email, paid_price) values(:1, :2, :3, :4)"
    cursor.executemany(insert, data)
    connection.commit()
    print("ticket created...")
    cursor.close()

def booking(connection, choosen_flight, email):
    flightno = choosen_flight[0][0]
    flightno2 = choosen_flight[0][1]
    dep_date = choosen_flight[0][4]
    fare = choosen_flight[0][9]
    paid_price = choosen_flight[0][11]
    #email = "bashir1@ualberta.ca"
    name = input("Name: ").title()
    passenger(connection, name, email)
    #does not check if ticket already exists, but it creates a very large random number
    tno = random.randint(199999999, 999999999)
    ticket(connection, tno, name, email, paid_price)
    print("creating booking...")
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    seat = str(random.randint(1,20))+random.choice(letters)
    data = [(tno, flightno, fare, dep_date, seat)]
    cursor = connection.cursor()
    insert = "insert into bookings(tno, flightno, fare, dep_date, seat) values (:1, :2, :3, :4, :5)"
    cursor.executemany(insert, data)
    connection.commit()
    cursor.close()
    if flightno2 != None:
        seat = str(random.randint(1,20))+random.choice(letters)
        data = [(tno, flightno2, fare, dep_date, seat)]
        cursor = connection.cursor()
        insert = "insert into bookings(tno, flightno, fare, dep_date, seat) values (:1, :2, :3, :4, :5)"
        cursor.executemany(insert, data)
        connection.commit()
        cursor.close()
    print("ticket number %d has been created successfully" % (tno))
    choice = input("Exit (exit) or Return to main menu (return): ")
    if choice == "exit" or choice == "e":
        exit()
    else:
        pass
    #ERROR MESSAGES IF BOOKING FAILED.
def list_bookings(connection, email):
    cursor = connection.cursor()
    select = "select b.tno, t.name, t.email, b.dep_date, t.paid_price, b.flightno, b.seat, b.fare"
    query = "%s from bookings b, tickets t where t.tno = b.tno and t.email = '%s'" % (select, email)
    cursor.execute(query)
    rows = cursor.fetchall()
    if rows == []:
        print("No bookings found, returning to the main menu in 2 seconds.")
        time.sleep(2)
        pass
    else:
        for i in range(0, len(rows)):
            print(i, rows[i][0:-3])
        choice = input("Select booking or return (return): ")
        if choice == 'return' or choice == 'r':
            pass
        else:
            choice = int(choice)
            os.system('clear')
            print("====================")
            print("Booking Information")
            print("====================")
            print("passenger name:", rows[choice][1])
            print("ticket number:", rows[choice][0])
            print("flight number:", rows[choice][-3])
            print("seat:", rows[choice][-2])
            print("fare type:", rows[choice][-1])
            print("price:", rows[choice][4])
            print("departure date:", rows[choice][3])
            print("returning to the main menu in 5 seconds.")
            time.sleep(5)
def cancel_booking(connection,  email):
    cursor = connection.cursor()
    name = input("Name: ")
    select = "select b.tno, t.name, t.email, b.dep_date, t.paid_price"
    query = "%s from bookings b, tickets t where t.tno = b.tno and t.name = '%s' and t.email = '%s'" % (select, name, email)
    cursor.execute(query)
    rows = cursor.fetchall()
    for i in range(0, len(rows)):
        print(i, rows[i][0])
    choice = input("Cancel a booking or return (return): ")
    if choice != 'return' or choice != 'r' and choice.isdigit():
        print("cancelling booking...")
        tno = rows[int(choice)][0]
        cursor.close()
        cursor = connection.cursor()
        query = "delete from bookings where tno = '%d'" % (tno)
        cursor.execute(query)
        connection.commit()
        print("booking cancelled!")
        print("returning to main menu in 2 seconds")
        time.sleep(2)
    else:
        print("return to main bookings")

def logout(connection, email):
    cursor = connection.cursor()
    update = "update users set last_login = sysdate where email = '%s'" % (email)
    cursor.execute(update)
    connection.commit()
    cursor.close()
    print("good bye")
    time.sleep(2)
def update(connection, dep):
    acode = input("Where are you (Enter in airport code): ")
    if dep == True:
        loc = 'src'
        field_to_update = 'act_dep_time'
    else:
        loc = 'dst'
        field_to_update = 'act_arr_time'
    today = datetime.datetime.today()
    day = today.day
    month = today.month
    year = today.year
    acode = acode.upper()
    sortby = "price"
    print("Searching for flights on %s/%s/%s..." %  (year, month, day))
    select = "flightno1, flightno2, src, dst, dep_time, arr_time, layover, stops, fare, seats, price"
    query = "select %s from search_flights where %s = '%s' and extract(month from dep_date) = '%s' and extract(day from dep_date) = '%s' and extract (year from dep_date) = '%s' order by %s" % (select, loc, acode, month, day, year, sortby)
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    if len(rows) > 0:
        for i in range(0, len(rows)):
            print(i, rows[i])
        choice = input("Please select flight ")
        if choice.isdigit():
            choice = int(choice)
            if dep == True:
                flightno = rows[choice][0]
            elif dep == False:
                if rows[choice][1] == None:
                    flightno = rows[choice][0]
                else:
                    flightno = rows[choice][1]
            cursor.close()
            cursor = connection.cursor()
            query = "select * from sch_flights where flightno = '%s' and extract(month from dep_date) = '%s' and extract(day from dep_date) = '%s' and extract (year from dep_date) = '%s'" % (flightno,  month, day, year)
            cursor.execute(query)
            rows = cursor.fetchall()
            print(flightno)
            for i in range(0, len(rows)):
                print(i, rows[i])
            choice = input("Update departure (update) or exit ")
            if choice == "update" or choice == "u":
                cursor.close()
                cursor = connection.cursor()
                query = "update sch_flights set %s = sysdate where flightno = '%s' and extract(month from dep_date) = '%s' and extract(day from dep_date) = '%s' and extract (year from dep_date) = '%s'" % (field_to_update, flightno,  month, day, year)
                cursor.execute(query)
                connection.commit()
                cursor.close()
                print("updated")
    else:
        print("Unable to find flights, please update your search criteria")





