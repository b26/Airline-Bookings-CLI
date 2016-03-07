import random
import time
import os
import datetime
#searches for available flights based off the dst, src, and date inputed by
#the user. Returns information regarding the flight, including fare type, and
#layover time, if any.
def search(connection, choosen_flight):
    acode = acodes(connection)
    values = dates()
    src = acode[0]
    dst = acode[1]
    month = values[0]
    day = values[1]
    year = values[2]
    sortby = input("Sort by number of stops (yes or no)?: ")
    if sortby == 'y' or sortby == 'yes':
        sortby = 'stops, price'
    else:
        sortby = 'price'
    query = "select * from search_flights where src = '%s' and dst = '%s' and extract(month from dep_date)='%s' and extract(day from dep_date) = '%s' and extract (year from dep_date) = '%s' order by %s" % (src, dst, month, day, year, sortby)
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    if len(rows) > 0:
        for i in range(0, len(rows)):
            print(i, rows[i])
        booking = input("choose flight or press return to go to the main menu ")
        if booking == "":
            pass
        elif booking.isdigit() and int(booking) < len(rows):
            flight = int(booking)
            choosen_flight.append(rows[flight])
    else:
        input("Unable to find flights. Press any key to return to the main menu")

#Asks the user where they are going and also when
#Asks the user when they are coming back
#Returns all flights that are valid and sums the price. Lists them in decending order.
def round_trip(connection,email):
    acode = acodes(connection);
    src = acode[0]
    dst = acode[1]
    dst_ = src
    src_ = dst
    print("Choose departure date")
    values = dates()
    month1 = values[0]
    day1 = values[1]
    year1 = values[2]
    print("Choose return date")
    values2 = dates()
    month2 = values2[0]
    day2 = values2[1]
    year2 = values[2]
    select = "select s1.flightno1, s1.flightno2, s2.flightno1, s2.flightno2, s1.src, s1.dst, s1.dep_date as departure, s2.dep_date as return, s1.fare, (s1.price + s2.price) as price"
    query = " %s from search_flights s1, search_flights s2 where extract(month from s1.dep_date) = '%s' and extract(day from s1.dep_date) = '%s' and extract(year from s1.dep_date) = '%s' and s1.src = '%s' and s1.dst = '%s' and s2.dst = '%s' and s2.src = '%s' and extract(day from s2.dep_date) = '%s' and extract(month from s2.dep_date) = '%s' and extract(year from s2.dep_date) = '%s' order by (s1.price + s2.price)" % (select, month1, day1, year1, src, dst, dst_, src_,  day2, month2, year2)
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    if rows == []:
        print("no results found.")
    else:
        for i in range(0, len(rows)):
            print(i, rows[i])
        choice = input("Please select your flight ")
        if choice.isdigit() and int(choice) < len(rows):
            booking_round(connection, rows[int(choice)], email)
    cursor.close()

#checks the airport codes and finds similiar airports if an exact code is not entered.
def acodes(connection):
    src = input("Source: ")
    dst = input("Destination: ")
    if len(src) > 3:
        src = src.title()
        query_src = "select acode from airports where city like '%"+src+"%'"
        cursor_src = connection.cursor()
        cursor_src.execute(query_src)
        rows = cursor_src.fetchall()
        if len(rows) > 0:
            for i in range(0, len(rows)):
                print(i, '-', rows[i][0])
            choice = input("Please select which airport ")
            if choice.isdigit():
                src = rows[int(choice)][0]
            else:
                print("invalid choice. choosing the first airport.")
                src = rows[0][0]
            cursor_src.close()
        else:
            print("Unable to find source airport...")
    if len(dst) > 3:
        dst = dst.title()
        query_dst = "select acode from airports where city like '%"+dst+"%'"
        cursor_dst = connection.cursor()
        cursor_dst.execute(query_dst)
        rows = cursor_dst.fetchall()
        if len(rows) > 0:
            for i in range(0, len(rows)):
                print(i, '-', rows[i][0])
            choice = input("Please select which airport ")
            if choice.isdigit():
                dst = rows[int(choice)][0]
            else:
                print("invalid choice. choosing the first airport.")
                dst = rows[0][0]
        else:
            print("Unable to find destination airport...")
        cursor_dst.close()
    return [src.upper(), dst.upper()]

#Asks the user for dates and returns them as an array
def dates():
    year = input("Year: ")
    month = input("Month: ")
    day = input("Day: ")
    return [month, day, year]

#checks if a passenger exists. If it doesn't then it creates a new passenger
#with that name and asks for the country the passenger is from.
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
#creates a ticket and inserts it into the tables.
def ticket(connection, tno, name, email, paid_price):
    print("creating ticket...")
    data = [(tno, name, email, paid_price)]
    cursor = connection.cursor()
    insert = "insert into tickets(tno, name, email, paid_price) values(:1, :2, :3, :4)"
    cursor.executemany(insert, data)
    connection.commit()
    print("ticket created...")
    cursor.close()

#creates a random ticket number and adds it into the booking table
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
#handles only round trip bookings. creates a random ticket number and adds it into the booking table
def booking_round(connection, choosen_flight, email):
    os.system('clear')
    flightno = choosen_flight[0]
    flightno2 = choosen_flight[1]
    flightno3 = choosen_flight[2]
    flightno4 = choosen_flight[3]
    dep_date = choosen_flight[6]
    return_date = choosen_flight[7]
    fare = choosen_flight[-2]
    paid_price = choosen_flight[-1]
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
    if flightno3 != None:
        seat = str(random.randint(1,20))+random.choice(letters)
        data = [(tno, flightno3, fare, return_date, seat)]
        cursor = connection.cursor()
        insert = "insert into bookings(tno, flightno, fare, dep_date, seat) values (:1, :2, :3, :4, :5)"
        cursor.executemany(insert, data)
        connection.commit()
        cursor.close()
    if flightno4 != None:
        seat = str(random.randint(1,20))+random.choice(letters)
        data = [(tno, flightno4, fare, return_date, seat)]
        cursor = connection.cursor()
        insert = "insert into bookings(tno, flightno, fare, dep_date, seat) values (:1, :2, :3, :4, :5)"
        cursor.executemany(insert, data)
        connection.commit()
        cursor.close()
    print("ticket number %d has been created successfully" % (tno))
    input("Press any key to return to the main menu")

#lists all of the bookings made under a certain name.
def list_bookings(connection, email):
    cursor = connection.cursor()
    select = "select b.tno, t.name, b.dep_date, t.paid_price, b.flightno, b.seat, b.fare"
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
        choice = input("Select booking or press any key to return to the main menu")
        if choice == "":
            pass
        elif choice.isdigit():
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
            print("price:", rows[choice][3])
            print("departure date:", rows[choice][2])
            input("Press any key to return to the main menu")
    cursor.close()

#deletes a booking from the booking table and delete tno from tickets table.
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
    if choice.isdigit():
        print("cancelling booking...")
        tno = rows[int(choice)][0]
        cursor.close()
        cursor = connection.cursor()
        query = "delete from bookings where tno = '%d'" % (tno)
        cursor.execute(query)
        connection.commit()
        cursor.close()
        cursor = connection.cursor()
        query = "delete from tickets where tno = '%d'" % (tno)
        cursor.execute(query)
        connection.commit()
        cursor.close()
        print("booking cancelled!")
        print("returning to main menu in 2 seconds")
        time.sleep(2)
    else:
        print("return to main bookings")

#updates last_login field in users table for the current user.
def logout(connection, email):
    cursor = connection.cursor()
    update = "update users set last_login = sysdate where email = '%s'" % (email)
    cursor.execute(update)
    connection.commit()
    cursor.close()
    print("good bye")
    time.sleep(2)

#updates the actual arrival/departure date of a flight seclected by the agent. If dep is true, then the agent is watching departures.
#If dep is false, then agent is watching arrivals
#updates sch_flights table for the selected flightno.
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
                    #This handles connection flights. In connection flights, flightno2 is the one we want.
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
        input("Please press any key to return to the main menu")





