import datetime
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
            flightno = rows[choice][0]
            cursor.close()
            cursor = connection.cursor()
            query = "select * from sch_flights where flightno = '%s' and extract(month from dep_date) = '%s' and extract(day from dep_date) = '%s' and extract (year from dep_date) = '%s'" % (flightno,  month, day, year)
            cursor.execute(query)
            rows = cursor.fetchall()
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






