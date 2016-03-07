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
    field_name = input("Please a field name ")
    field_name_ = ''.join(field_name.split())
    connection = cx_Oracle.connect(connection_string)

    #make query
    query = "select * from c291.students where field = '%s'" % (field_name)

    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    names = []
    for name in cursor.description:
        names.append(name[0])
    #print(names)
    #createStr = ("create table '%s' ('%s' CHAR(30), SUP_ID CHAR(30), PRICE CHAR(30), SALES CHAR(30), TOTAL CHAR(30))")
    table_query = "create table %s (" % (field_name_)
    for name in names:
        table_query += "%s CHAR(30)," % (name)
    table_query += ")"
    table_tuple = (table_query)
    #del table_tuple[-2]
    #print(table_tuple)
    table_tuple = table_tuple[:-2] + table_tuple[-1]
    cursor2 = connection.cursor()
    cursor2.execute(table_tuple)
    connection.commit()
    insert_string = "INSERT INTO %s (" % (field_name_)
    values_string = "VALUES ("
    for i in range(0, len(names)):
        insert_string += "%s," % (names[i])
        values_string += ":%d," % (i+1)
    insert_string += ")"
    values_string += ")"
    insert_string = insert_string[:-2] + insert_string[-1]
    values_string = values_string[:-2] + values_string[-1]
    insert_string = (insert_string + " " + values_string)
    print(insert_string)
    for i in range(0, len(rows)):
        cursor3 = connection.cursor()
        cursor3.executemany(insert_string, [rows[i]])
        connection.commit()
        cursor3.close()
    #for row in rows:
        #cursor2.executemany(insert_string, [row]);
        #connection.commit()

    #for i in range(0, len(rows)):
        #print(cursor.description[i][0], rows[i][i])
        #print(i, rows[i])
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





