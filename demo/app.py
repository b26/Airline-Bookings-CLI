import os
from methods import *
import getpass
import datetime

#The App class handles everything the user is able to do.
#It also builds are login screen and any screens we need.
class App():

    #We initialize choice and choosen_flights because we need to save the values
    def __init__(self):
        self.choice = None
        self.choosen_flight = []

    #Loads the login screen and handles registration and user login
    def start(self, connection):
        agent = False
        os.system('clear')
        print("====================")
        print("Airline Application")
        print("====================")
        print("1 - Login")
        print("2 - Register")
        print("3 - Exit")
        choice = input(">> ")
        if choice == "1":
            email = input("Email [%s]: " % getpass.getuser())
            password = getpass.getpass()
            cursor = connection.cursor()
            query = "select * from users where email = '%s' and pass = '%s'" % (email, password)
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            if len(rows) == 0:
                print("Incorrect password or email")
                exit()
            else:
                cursor = connection.cursor()
                query = "select * from airline_agents where email = '%s'" % (email)
                cursor.execute(query)
                rows = cursor.fetchall()
                if rows == []:
                    agent = False
                else:
                    agent = True
                self.user_menu(connection, email, agent)
        elif choice == "2":
            email = input("Email: ")
            password = getpass.getpass()
            date = datetime.datetime.today()
            data = [(email, password, date)]
            cursor = connection.cursor()
            query = "insert into users(email, pass, last_login) values(:1, :2, :3)"
            cursor.executemany(query, data)
            connection.commit()
            self.user_menu(connection, email, agent)
        elif choice == "3":
            print("Exiting program.")
            exit()
        else:
            print("Invalid choice. Exiting program ")
            exit()

    #Loads our user menu. It also handles if the current user is an agent.
    def user_menu(self, connection, email, agent):
        os.system('clear')
        print("====================")
        print("Airline Application")
        print("====================")
        print("Please choose the menu you want to start:")
        print("1 - Search - One-way flights")
        print("2 - Search - Round-trip")
        print("3 - List existing bookings")
        print("4 - Cancel a booking")
        if agent:
            print("5 - Agent Departures")
            print("6 - Agent Arrivals")
        print("E - Logout")
        self.choice = input(">> ")
        if self.choice == "1":
            self.search_flights(connection, email, agent)
        elif self.choice == "3":
            self.listing(connection, email, agent)
        elif self.choice == "4":
            self.cancel_booking(connection, email, agent)
        elif self.choice == "E":
            self.exit_app(connection, email)
        elif self.choice == "5" and agent:
            os.system('clear')
            self.update(connection, email, agent, True)
        elif self.choice == "6" and agent:
            os.system('clear')
            self.update(connection, email, agent, False)
        elif self.choice == "2":
            os.system('clear')
            self.search_round(connection,  email, agent)
        else:
            print("invalid choice")
            self.user_menu(connection, email, agent)

    #Loads screen for one way flights and calls search from methods.py
    def search_flights(self, connection, email, agent):
        os.system('clear')
        print("=======================")
        print("Search One-way Flights")
        print("=======================")
        search(connection, self.choosen_flight)
        print(self.choosen_flight)
        if self.choosen_flight == []:
            self.user_menu(connection, email, agent)
        else:
            self.make_booking(connection, email, agent)
        self.exit_app(connection, email)

    #Loads screen for round trip flights and calls round_trip from methods.py
    def search_round(self, connection, email, agent):
        os.system('clear')
        print("==========================")
        print("Search Round-Trip Flights")
        print("==========================")
        round_trip(connection, email)
        self.user_menu(connection, email, agent)

    #Loads make a booking screen and calls booking from manage.py
    def make_booking(self, connection, email, agent):
        os.system('clear')
        print("===============")
        print("Make a booking")
        print("===============")
        booking(connection, self.choosen_flight, email)
        self.choosen_flight = []
        self.user_menu(connection, email, agent)

   #Loads existing bookings screen and calls list_bookings from methods.py
    def listing(self, connection, email, agent):
        os.system('clear')
        print("=======================")
        print("List existing bookings")
        print("=======================")
        list_bookings(connection, email)
        self.user_menu(connection, email, agent)
        #exit()

    #Loads cancel a booking screen and calls cancel_booking from methods.py
    def cancel_booking(self, connection, email, agent):
        os.system('clear')
        print("=================")
        print("Cancel a Booking")
        print("=================")
        cancel_booking(connection, email)
        self.user_menu(connection, email, agent)
        #exit()

    #Loads update flight screen and calls update from method.py. This will only show if you're an agent
    def update(self, connection, email, agent, dep):
        os.system('clear')
        print("=================")
        print("Update Flight")
        print("=================")
        update(connection, dep)
        self.user_menu(connection, email, agent)

    #Calls logout from manage.py then exits the application
    def exit_app(self, connection, email):
        os.system('clear')
        logout(connection, email)
        exit()

