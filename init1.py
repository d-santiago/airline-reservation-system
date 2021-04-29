#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import datetime

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=8889,
                       user='root',
                       password='root',
                       db='Air_Ticket_Reservation_System',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to index page
@app.route('/', methods=['GET', 'POST'])
def index():

	# When a customer clicks the "Search" button under 'Search for Flights', a flight search will be conducted (conduct_flight_search = True)
	# We know when a customer clicks this button if we recieve 'trip_type', 'source', 'destination', 'departure', and 'arrival' in the the 'POST' Form
	conduct_flight_search = False
	if ('trip_type' in request.form and 'source' in request.form and 'destination' in request.form and 'departure' in request.form and 'arrival' in request.form):	
		conduct_flight_search = True
		trip_type = request.form['trip_type']
		source = request.form['source']
		destination = request.form['destination']	
		departure = request.form['departure']
		arrival = request.form['arrival']


	# When a customer clicks the "Search" button under 'Get Flight Status', a flight status search will be conducted (conduct_get_status = True)
	# We know when a customer clicks this button if we recieve 'airline_name', 'flight_num', 'departure', and 'arrival' in the the 'POST' Form
	get_flight_status = False
	if ('airline_name' in request.form and 'flight_num' in request.form and 'departure' in request.form and 'arrival' in request.form):	
		get_flight_status = True
		airline_name = request.form['airline_name']
		flight_num = request.form['flight_num']
		departure = request.form['departure']
		arrival = request.form['arrival']
	

	# establish connection with PHPMyAdmin
	cursor = conn.cursor()


	# When a customer clicks the "Search" button under 'Search for and Purchase Flights', a flight serarch will be conducted (conduct_flight_search = True)
	if (conduct_flight_search == True):
		# search_flights = 'SELECT * FROM Flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_date = %s AND arrival_date = %s AND trip_type = %s AND departure_date >= DATE(NOW()) AND arrival_date >= DATE(NOW())'
		# cursor.execute(search_flights, (source, destination, departure, arrival, trip_type))
		search_flights = 'SELECT * FROM Flight WHERE departure_airport = %s AND arrival_airport = %s AND trip_type = %s AND departure_date >= %s AND arrival_date <= %s'				
		cursor.execute(search_flights, (source, destination, trip_type, departure, arrival))
		query_flights = cursor.fetchall()

		if (not query_flights):
			query_flights = "No Results"

		cursor.close()
		return render_template('index.html', query_flights=query_flights)


	# When a customer clicks the "Search" button under 'Get Flight Status', a flight status search will be conducted (conduct_get_status = True)
	if (get_flight_status == True):
		search_flights = 'SELECT flight_status FROM Flight WHERE airline_name = %s AND flight_num = %s AND departure_date = %s AND arrival_date = %s'				
		cursor.execute(search_flights, (airline_name, flight_num, departure, arrival))
		flight_status = cursor.fetchone()

		if (not flight_status):
			flight_status="No Results"
		else:
			flight_status = flight_status['flight_status']

		cursor.close()
		return render_template('index.html', flight_num=flight_num, flight_status=flight_status)


	return render_template('index.html')

#Define route for the Customer's login
@app.route('/customerLogin')
def customerlogin():
	return render_template('customerLogin.html')

#Define route for the Booking Agent's login
@app.route('/agentLogin')
def agentLogin():
	return render_template('agentLogin.html')

#Define route for the Airline Staff's login
@app.route('/staffLogin')
def staffLogin():
	return render_template('staffLogin.html')

#Define route for the Customer's registration
@app.route('/customerRegistration')
def customerRegistration():
	return render_template('customerRegistration.html')

#Define route for the Booking Agent's registration
@app.route('/agentRegistration')
def agentRegistration():
	return render_template('agentRegistration.html')

#Define route for the Airline Staff's registration
@app.route('/staffRegistration')
def staffRegistration():
	return render_template('staffRegistration.html')

#Authenticates the Customer's Login
@app.route('/customerLoginAuth', methods=['GET', 'POST'])
def customerLoginAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE cus_email = %s and cus_password = MD5(%s)'
	cursor.execute(query, (email, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = email
		return redirect(url_for('customerHome'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('customerLogin.html', error=error)


#Authenticates the Booking Agent's Login
@app.route('/agentLoginAuth', methods=['GET', 'POST'])
def agentLoginAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Booking_Agent WHERE agent_email = %s and agent_password = MD5(%s)'
	cursor.execute(query, (email, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = email
		return redirect(url_for('agentHome'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('agentLogin.html', error=error)


#Authenticates the Airline Staff's Login
@app.route('/staffLoginAuth', methods=['GET', 'POST'])
def staffLoginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Airline_Staff WHERE staff_username = %s and staff_password = MD5(%s)'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('staffHome'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('staffLogin.html', error=error)

# Authenticates the Customer's registration
@app.route('/customerRegistrationAuth', methods=['GET', 'POST'])
def customerRegistrationAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	name = request.form['name']
	buildingNum = request.form['buildingNum']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	phone = request.form['phone']
	dob = request.form['dob']
	passportNum = request.form['passportNum']
	passportExp = request.form['passportExp']
	passportCountry = request.form['passportCountry']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Customer WHERE cus_email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This customer already exists"
		return render_template('customerRegistration.html', error = error)
	else:
		ins = 'INSERT INTO Customer VALUES(%s, %s, MD5(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (name, email, password, buildingNum, street, city, state, phone, dob, passportNum, passportExp, passportCountry))
		conn.commit()
		cursor.close()
		return render_template('index.html')

# Authenticates the Booking Agent's registration
@app.route('/agentRegistrationAuth', methods=['GET', 'POST'])
def agentRegistrationAuth():
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password']
	airline = request.form['airline']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Booking_Agent WHERE agent_email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This booking agent already exists"
		return render_template('agentRegistration.html', error = error)
	else:
		ins = 'INSERT INTO Booking_Agent (agent_email, agent_password, airline_name) VALUES(%s, MD5(%s), %s)'
		cursor.execute(ins, (email, password, airline))
		conn.commit()
		cursor.close()
		return render_template('index.html')

# Authenticates the Airline Staff's registration
@app.route('/staffRegistrationAuth', methods=['GET', 'POST'])
def staffRegistrationAuth():
	#grabs information from the forms
	firstName = request.form['firstName']
	lastName = request.form['lastName']
	password = request.form['password']
	username = request.form['username']
	dob = request.form['dob']
	phone = request.form['phone']
	airline = request.form['airline']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM Airline_Staff WHERE staff_username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This airline stafff member already exists"
		return render_template('staffRegistration.html', error = error)
	else:
		ins = 'INSERT INTO Airline_Staff VALUES(%s, %s, %s, MD5(%s), %s, %s, %s)'
		cursor.execute(ins, (firstName, lastName, username, password, dob, phone, airline))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/customerHome', methods=['GET', 'POST'])
def customerHome():
	username = session['username']


	# When a customer clicks the "Search" button under 'Search for and Purchase Flights', a flight serarch will be conducted (conduct_flight_search = True)
	# We know when a customer clicks this button if we recieve 'trip_type', 'source', 'destination', 'departure', and 'arrival' in the the 'POST' Form
	conduct_flight_search = False
	if ('trip_type' in request.form and 'source' in request.form and 'destination' in request.form and 'departure' in request.form and 'arrival' in request.form):	
		conduct_flight_search = True
		trip_type = request.form['trip_type']
		source = request.form['source']
		destination = request.form['destination']	
		departure = request.form['departure']
		arrival = request.form['arrival']


	# When a customer clicks the "Yes" button under 'Check Availability' for a certain flight, a ticket serarch will be conducted (conduct_ticket_search = True) for that flight.
	# A purchase form will be revealed if there are tickets avaiable.
	# We know when a customer clicks this button if we recieve 'flight_select' in the the 'POST' Form
	conduct_ticket_search = False
	if ('flight_select' in request.form):
		conduct_ticket_search = True
		flight_select = request.form['flight_select']


	# When a customer clicks the "Purchase" button under 'Purchase Tickets', a ticket purchase will be conducted (conduct_ticket_purchase = True)
	# We know when a customer clicks this button if we recieve 'flight_purchase', 'ticket', 'type', 'num', 'name', and 'exp' in the the 'POST' Form
	conduct_ticket_purchase = False;
	if ('flight_purchase' in request.form and 'ticket' in request.form and 'type' in request.form and 'num' in request.form and 'name' in request.form and 'exp' in request.form):	
		conduct_ticket_purchase = True
		flight_purchase = request.form['flight_purchase']
		ticket_IDs = request.form.getlist('ticket')
		card_type = request.form['type']
		card_num = request.form['num']
		card_name = request.form['name']
		card_exp = request.form['exp']	


	# When a customer clicks the "Yes" button under 'Rate and Review', a form will be revealed to the user under 'Review Previously Taken Flights' (reveal_review_form = True)
	# We know when a customer clicks this button if we recieve 'flight_to_rate' in the the 'POST' Form
	reveal_review_form = False
	if ('flight_to_rate' in request.form):	
		reveal_review_form = True
		flight_to_rate = request.form['flight_to_rate']


	# When a customer clicks the "Submit" button under 'Review Previously Taken Flights', their review will be submitted (submit_rating = True)
	# We know when a customer clicks this button if we recieve 'flight_rated' in the the 'POST' Form
	submit_rating = False;
	if ('flight_rated' in request.form and 'rating' in request.form and 'comment' in request.form):	
		submit_rating = True;
		flight_rated = request.form['flight_rated']
		rating = request.form['rating']
		comment = request.form['comment']


	# When a customer clicks the "Search" button under 'My Spending', the program will determine how much money that customer spent between two user-specified dates (track_spending = True)
	# We know when a customer clicks this button if we recieve 'start_date' and 'end_date' in the the 'POST' Form
	track_spending = False;
	if ('start_date' in request.form and 'end_date' in request.form):	
		track_spending = True;
		start_date = request.form['start_date']
		end_date = request.form['end_date']


	######################################################################THIS CODE RUNS EVERYTIME THE PAGE IS LOADED OR REFRESHED######################################################################

	# establish connection with PHPMyAdmin
	cursor = conn.cursor()
	
	# When the page is loaded or refreshed, the program finds all flights that a customer has purchased from Customer_Purchases Table using their email
	find_flights = 'SELECT flight_num, ticket_ID FROM Customer_Purchases WHERE cus_email = %s'
	cursor.execute(find_flights, (username))
	all_flights = cursor.fetchall()

	all_flights_info = []
	past_flights_info = []
	future_flights_info = []

	flightsOccured = []

	# When the page is loaded or refreshed, the program finds additinoal information about each flight that isn't stored in the Cutomer_Purchases Table using the Flight Table
	for flight in all_flights:

		# Prevents duplicate flight information from being selected
		if (flight['flight_num'] not in flightsOccured):

			find_all_flights_info = 'SELECT * FROM Flight WHERE flight_num = %s'

			cursor.execute(find_all_flights_info, (flight['flight_num']))
			flight_info = cursor.fetchone()
			all_flights_info.append(flight_info)

			flightsOccured.append(flight['flight_num'])


	# When the page is loaded or refreshed, the program finds additinoal information about each PAST flight that isn't stored in the Cutomer_Purchases Table using the Flight Table
	flightsOccured = []
	for flight in all_flights:

		# Prevents duplicate flight information from being selected
		if (flight['flight_num'] not in flightsOccured):

			find_past_flights_info = 'SELECT * FROM Flight WHERE flight_num = %s AND departure_date < DATE(NOW())'

			cursor.execute(find_past_flights_info, (flight['flight_num']))
			flight_info = cursor.fetchone()
			past_flights_info.append(flight_info)

			flightsOccured.append(flight['flight_num'])


	# When the page is loaded or refreshed, the program finds additinoal information about each FUTURE flight that isn't stored in the Cutomer_Purchases Table using the Flight Table
	flightsOccured = []
	for flight in all_flights:

		# Prevents duplicate flight information from being selected
		if (flight['flight_num'] not in flightsOccured):

			find_future_flights_info = 'SELECT * FROM Flight WHERE flight_num = %s AND departure_date > DATE(NOW())'

			cursor.execute(find_future_flights_info, (flight['flight_num']))
			flight_info = cursor.fetchone()
			future_flights_info.append(flight_info)

			flightsOccured.append(flight['flight_num'])


	# When the page is loaded or refreshed, the program calculates the customer's expenses within the past year by finding the sum of the sold_prices for the tickets in the Customer_Purchases table using their email
	calc_year_expenses = 'SELECT SUM(sold_price) AS year_expenses FROM Customer_Purchases WHERE cus_email = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 YEAR)'
	cursor.execute(calc_year_expenses, (username))
	year_expenses = cursor.fetchone()
	year_expenses = year_expenses['year_expenses']

	if (year_expenses == None):
		year_expenses='0.0'
		
	######################################################################THIS CODE RUNS EVERYTIME THE PAGE IS LOADED OR REFRESHED######################################################################


	# When a customer clicks the "Search" button under 'Search for and Purchase Flights', a flight serarch will be conducted (conduct_flight_search = True)
	if (conduct_flight_search == True):
		# search_flights = 'SELECT * FROM Flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_date = %s AND arrival_date = %s AND trip_type = %s AND departure_date >= DATE(NOW()) AND arrival_date >= DATE(NOW())'
		# cursor.execute(search_flights, (source, destination, departure, arrival, trip_type))
		search_flights = 'SELECT * FROM Flight WHERE departure_airport = %s AND arrival_airport = %s AND trip_type = %s AND departure_date >= %s AND arrival_date <= %s'				
		cursor.execute(search_flights, (source, destination, trip_type, departure, arrival))
		query_flights = cursor.fetchall()

		if (not query_flights):
			query_flights = "No Results"

		cursor.close()
		return render_template('customerHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, query_flights=query_flights, year_expenses=year_expenses)


	# When a customer clicks the "Yes" button under 'Check Availability' for a certain flight, a ticket serarch will be conducted (conduct_ticket_search = True) for that flight.
	# A purchase form will be revealed if there are tickets avaiable.
	if (conduct_ticket_search == True):
		search_tickets = 'SELECT ticket_ID FROM Ticket WHERE flight_num = %s AND is_purchased = "No"'
		cursor.execute(search_tickets, (flight_select))
		tickets = cursor.fetchall()

		if (not tickets):
			tickets = "No Tickets"

		cursor.close()
		return render_template('customerHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, year_expenses=year_expenses, flight_select=flight_select, tickets=tickets)


	# When a customer clicks the "Purchase" button under 'Purchase Tickets', a ticket purchase will be conducted (conduct_ticket_purchase = True)
	# A purchase is completed by updating the ticket's is_Purchased field from 'No' to 'Yes' in the Ticket Table and inserting the customer's 'POST' form information into the Customer_Purchases table
	if (conduct_ticket_purchase == True):

		for ticket_ID in ticket_IDs:

			search_tickets = 'SELECT is_Purchased FROM Ticket WHERE ticket_ID = %s'
			cursor.execute(search_tickets, (ticket_ID))
			is_Purchased = cursor.fetchone()
			is_Purchased = is_Purchased['is_Purchased']

			if(is_Purchased == "No"):

				change_ticket_status = 'UPDATE Ticket SET is_purchased = "Yes" WHERE ticket_ID = %s AND is_purchased = "No"'
				cursor.execute(change_ticket_status, (ticket_ID))
				conn.commit()

				# Find the base_price and airplane_ID for the flight
				find_flight_info = 'SELECT base_price, airplane_ID FROM Flight WHERE flight_num = %s'
				cursor.execute(find_flight_info, (flight_purchase))
				flight_info = cursor.fetchone()
				base_price = flight_info['base_price']
				airplane_ID = flight_info['airplane_ID']

				# Using the airplane_ID, finr the seats on that plane
				find_seats = 'SELECT seats FROM Airplane WHERE airplane_ID = %s'
				cursor.execute(find_seats, (airplane_ID))
				seats = cursor.fetchone()
				seats = int(seats['seats'])

				# Count the number of tickets purchased for the flight
				count_tickets_purchased = 'SELECT COUNT(ticket_ID) AS tickets_purchased FROM Customer_Purchases WHERE flight_num = %s'
				cursor.execute(count_tickets_purchased, (flight_purchase))
				tickets_purchased = cursor.fetchone()
				tickets_purchased = int(tickets_purchased['tickets_purchased'])

				# Determine the capacity of the flight by dividing the number of tickets purchased by the number of seats on the airplane
				capacity = (tickets_purchased / seats) * 100

				# If the capacity of the flight> 70, the sold price is 1.2 * base_price
				if(capacity > 70):
					sold_price = base_price * 1.2
				else:
					sold_price = base_price

				insert_purchase = 'INSERT INTO CUSTOMER_PURCHASES (cus_email, ticket_ID, flight_num, sold_price, card_type, card_num, card_name, card_exp_date, \
									purchase_date, purchase_time, agent_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, DATE(NOW()), TIME(NOW()), NULL)'

				cursor.execute(insert_purchase, (username, ticket_ID, flight_purchase, sold_price, card_type, card_num, card_name, card_exp))
				conn.commit()

		cursor.close()
		return render_template('customerHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, year_expenses=year_expenses, purchase="Complete")


	# When a customer clicks the "Yes" button under 'Rate and Review', a form will be revealed to the user under 'Review Previously Taken Flights' (reveal_review_form = True)
	# A customer who has already reviewed a flight will not be able to review it again
	if (reveal_review_form == True):
		search_tickets = 'SELECT * FROM Review WHERE flight_num = %s AND cus_email = %s'
		cursor.execute(search_tickets, (flight_to_rate, username))
		isFlightRated = cursor.fetchall()

		if (not isFlightRated):
			cursor.close()
			return render_template('customerHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
									past_flights_info=past_flights_info, future_flights_info=future_flights_info, year_expenses=year_expenses, flight_to_rate=flight_to_rate)
		else:
			cursor.close()
			return render_template('customerHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
									past_flights_info=past_flights_info, future_flights_info=future_flights_info, year_expenses=year_expenses, flight_rated=flight_to_rate, review="Already Complete")


	# When a customer clicks the "Submit" button under 'Review Previously Taken Flights', their review will be submitted (submit_rating = True)
	if (submit_rating == True):
		change_ticket_status = 'INSERT INTO Review(cus_email, flight_num, rating, comment) VALUES(%s, %s, %s, %s)'
		cursor.execute(change_ticket_status, (username, flight_rated, rating, comment))
		conn.commit()

		cursor.close()
		# return render_template('customerHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
							# past_flights_info=past_flights_info, future_flights_info=future_flights_info, year_expenses=year_expenses, review="Complete")
		return redirect(url_for('customerHome'))

	
	# When a customer clicks the "Search" button under 'My Spending', the program will determine how much money that customer spent between two user-specified dates (track_spending = True)
	if (track_spending == True):
		calc_date_expenses = 'SELECT SUM(sold_price) AS date_expenses FROM Customer_Purchases WHERE cus_email = %s AND purchase_date >= %s AND purchase_date <= %s'
		cursor.execute(calc_date_expenses, (username, start_date, end_date))
		date_expenses = cursor.fetchone()
		date_expenses = date_expenses['date_expenses']

		if (date_expenses == None):
			date_expenses="0.0"

		cursor.close()
		return render_template('customerHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, year_expenses=year_expenses, \
								date_expenses=date_expenses, start_date=start_date, end_date=end_date)


	# Returns default information that is displayed each time the page is loaded or refreshed
	cursor.close()
	return render_template('customerHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
							past_flights_info=past_flights_info, future_flights_info=future_flights_info, year_expenses=year_expenses)

@app.route('/agentHome', methods=['GET', 'POST'])
def agentHome():
	username = session['username']

	# When a booking agent clicks the "Search" button under 'Search for and Purchase Flights', a flight serarch will be conducted (conduct_flight_search = True)
	# We know when a booking agent clicks this button if we recieve 'trip_type', 'source', 'destination', 'departure', and 'arrival' in the the 'POST' Form
	conduct_flight_search = False
	if ('trip_type' in request.form and 'source' in request.form and 'destination' in request.form and 'departure' in request.form and 'arrival' in request.form):	
		conduct_flight_search = True
		trip_type = request.form['trip_type']
		source = request.form['source']
		destination = request.form['destination']	
		departure = request.form['departure']
		arrival = request.form['arrival']


	# When a booking agent clicks the "Yes" button under 'Check Availability' for a certain flight, a ticket serarch will be conducted (conduct_ticket_search = True) for that flight.
	# A purchase form will be revealed if there are tickets avaiable.
	# We know when a booking agent clicks this button if we recieve 'flight_select' in the the 'POST' Form
	conduct_ticket_search = False
	if ('flight_select' in request.form):
		conduct_ticket_search = True
		flight_select = request.form['flight_select']


	# When a booking agent clicks the "Purchase" button under 'Purchase Tickets', a ticket purchase will be conducted (conduct_ticket_purchase = True)
	# We know when a booking agent clicks this button if we recieve 'flight_purchase', 'ticket', 'type', 'num', 'name', and 'exp' in the the 'POST' Form
	conduct_ticket_purchase = False;
	if ('flight_purchase' in request.form and 'cus_email' in request.form and 'ticket' in request.form and 'type' in request.form and 'num' in request.form and 'name' in request.form and 'exp' in request.form):	
		conduct_ticket_purchase = True
		flight_purchase = request.form['flight_purchase']
		cus_email = request.form['cus_email']
		ticket_IDs = request.form.getlist('ticket')
		card_type = request.form['type']
		card_num = request.form['num']
		card_name = request.form['name']
		card_exp = request.form['exp']

	# When a customer clicks the "Search" button under 'My Spending', the program will determine how much money that customer spent between two user-specified dates (track_spending = True)
	# We know when a customer clicks this button if we recieve 'start_date' and 'end_date' in the the 'POST' Form
	track_commission = False;
	if ('start_date' in request.form and 'end_date' in request.form):	
		track_commission = True;
		start_date = request.form['start_date']
		end_date = request.form['end_date']


	######################################################################THIS CODE RUNS EVERYTIME THE PAGE IS LOADED OR REFRESHED######################################################################

	# establish connection with PHPMyAdmin
	cursor = conn.cursor()
	
	# When the page is loaded or refreshed, the program finds the agent_ID of the booking agent using their email in the Customer_Purchases Table
	find_agent_ID = 'SELECT agent_ID FROM Booking_Agent WHERE agent_email = %s'
	cursor.execute(find_agent_ID, (username))
	agent_ID = cursor.fetchone()
	agent_ID = agent_ID['agent_ID']	

	# When the page is loaded or refreshed, the program finds all flights that a booking agent has purchased from Customer_Purchases Table using their email
	find_flights = 'SELECT cus_email, flight_num, ticket_ID FROM Customer_Purchases WHERE agent_ID = %s'
	cursor.execute(find_flights, (agent_ID))
	all_flights = cursor.fetchall()

	all_flights_info = []
	past_flights_info = []
	future_flights_info = []

	flightsOccured = []

	# When the page is loaded or refreshed, the program finds additinoal information about each flight that isn't stored in the Cutomer_Purchases Table using the Flight Table
	for flight in all_flights:

		# Prevents duplicate flight information from being selected
		if (flight['flight_num'] not in flightsOccured):

			find_all_flights_info = 'SELECT * FROM Flight WHERE flight_num = %s'

			cursor.execute(find_all_flights_info, (flight['flight_num']))
			flight_info = cursor.fetchone()
			all_flights_info.append(flight_info)

			flightsOccured.append(flight['flight_num'])


	# When the page is loaded or refreshed, the program finds additinoal information about each PAST flight that isn't stored in the Cutomer_Purchases Table using the Flight Table
	flightsOccured = []
	for flight in all_flights:

		# Prevents duplicate flight information from being selected
		if (flight['flight_num'] not in flightsOccured):

			find_past_flights_info = 'SELECT * FROM Flight WHERE flight_num = %s AND departure_date < DATE(NOW())'

			cursor.execute(find_past_flights_info, (flight['flight_num']))
			flight_info = cursor.fetchone()
			past_flights_info.append(flight_info)

			flightsOccured.append(flight['flight_num'])


	# When the page is loaded or refreshed, the program finds additinoal information about each FUTURE flight that isn't stored in the Cutomer_Purchases Table using the Flight Table
	flightsOccured = []
	for flight in all_flights:

		# Prevents duplicate flight information from being selected
		if (flight['flight_num'] not in flightsOccured):

			find_future_flights_info = 'SELECT * FROM Flight WHERE flight_num = %s AND departure_date > DATE(NOW())'

			cursor.execute(find_future_flights_info, (flight['flight_num']))
			flight_info = cursor.fetchone()
			future_flights_info.append(flight_info)

			flightsOccured.append(flight['flight_num'])


	# When the page is loaded or refreshed, the program calculates the customer's expenses within the past year by finding the sum of the sold_prices for the tickets in the Customer_Purchases table using their email
	calc_commission = 'SELECT SUM(sold_price) AS commission, COUNT(ticket_ID) AS tickets_sold FROM Customer_Purchases WHERE agent_ID = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 30 DAY)'
	cursor.execute(calc_commission, (agent_ID))
	commission_info = cursor.fetchone()
	commission = commission_info['commission']

	if (commission == None):
		commission='0.0'
		comm_per_ticket = '0.0'
		tickets_sold = 0
	else:
		commission = int(commission) * 0.1
		tickets_sold = int(commission_info['tickets_sold'])
		comm_per_ticket = commission / tickets_sold

	# find_customers = 'SELECT SUM(sold_price) cus_email FROM Customer_Purchases WHERE agent_ID = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 6 MONTH)'
	find_customers = 'SELECT cus_email, SUM(sold_price) * 0.1 as cus_commission FROM Customer_Purchases WHERE agent_ID = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 6 MONTH) GROUP BY cus_email ORDER BY cus_commission DESC LIMIT 0, 5'
	cursor.execute(find_customers, (agent_ID))
	top_customers_month = cursor.fetchall()

	# find_customers = 'SELECT SUM(sold_price) cus_email FROM Customer_Purchases WHERE agent_ID = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 6 MONTH)'
	find_customers = 'SELECT cus_email, SUM(sold_price) * 0.1 as cus_commission FROM Customer_Purchases WHERE agent_ID = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 YEAR) GROUP BY cus_email ORDER BY cus_commission DESC LIMIT 0, 5'
	cursor.execute(find_customers, (agent_ID))
	top_customers_year = cursor.fetchall()

	######################################################################THIS CODE RUNS EVERYTIME THE PAGE IS LOADED OR REFRESHED######################################################################


	# When a customer clicks the "Search" button under 'Search for and Purchase Flights', a flight serarch will be conducted (conduct_flight_search = True)
	if (conduct_flight_search == True):
		# search_flights = 'SELECT * FROM Flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_date = %s AND arrival_date = %s AND trip_type = %s AND departure_date >= DATE(NOW()) AND arrival_date >= DATE(NOW())'			
		# cursor.execute(search_flights, (source, destination, departure, arrival, trip_type))
		search_flights = 'SELECT * FROM Flight WHERE departure_airport = %s AND arrival_airport = %s AND trip_type = %s AND departure_date >= %s AND arrival_date <= %s'				
		cursor.execute(search_flights, (source, destination, trip_type, departure, arrival))
		query_flights = cursor.fetchall()

		if (not query_flights):
			query_flights = "No Results"

		cursor.close()
		return render_template('agentHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, month_commission=month_commission, \
								month_tickets_sold=tickets_sold, month_comm_per_ticket=comm_per_ticket, top_customers_month=top_customers_month, \
								top_customers_year=top_customers_year, query_flights=query_flights)


	# When a booking agent clicks the "Yes" button under 'Check Availability' for a certain flight, a ticket serarch will be conducted (conduct_ticket_search = True) for that flight.
	# A purchase form will be revealed if there are tickets avaiable.
	if (conduct_ticket_search == True):
		search_tickets = 'SELECT ticket_ID FROM Ticket WHERE flight_num = %s AND is_purchased = "No"'
		cursor.execute(search_tickets, (flight_select))
		tickets = cursor.fetchall()

		if (not tickets):
			tickets = "No Tickets"

		cursor.close()
		return render_template('agentHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, month_commission=month_commission, \
								month_tickets_sold=tickets_sold, month_comm_per_ticket=comm_per_ticket, top_customers_month=top_customers_month, \
								top_customers_year=top_customers_year, flight_select=flight_select, tickets=tickets)


	# When a booking agent clicks the "Purchase" button under 'Purchase Tickets', a ticket purchase will be conducted (conduct_ticket_purchase = True)
	# A purchase is completed by updating the ticket's is_Purchased field from 'No' to 'Yes' in the Ticket Table and inserting the booking agent's 'POST' form information into the Customer_Purchases table
	if (conduct_ticket_purchase == True):

		for ticket_ID in ticket_IDs:

			search_tickets = 'SELECT is_Purchased FROM Ticket WHERE ticket_ID = %s'
			cursor.execute(search_tickets, (ticket_ID))
			is_Purchased = cursor.fetchone()
			is_Purchased = is_Purchased['is_Purchased']

			if(is_Purchased == "No"):

				change_ticket_status = 'UPDATE Ticket SET is_purchased = "Yes" WHERE ticket_ID = %s AND is_purchased = "No"'
				cursor.execute(change_ticket_status, (ticket_ID))
				conn.commit()

				# Find the base_price and airplane_ID for the flight
				find_flight_info = 'SELECT base_price, airplane_ID FROM Flight WHERE flight_num = %s'
				cursor.execute(find_flight_info, (flight_purchase))
				flight_info = cursor.fetchone()
				base_price = flight_info['base_price']
				airplane_ID = flight_info['airplane_ID']

				# Using the airplane_ID, finr the seats on that plane
				find_seats = 'SELECT seats FROM Airplane WHERE airplane_ID = %s'
				cursor.execute(find_seats, (airplane_ID))
				seats = cursor.fetchone()
				seats = int(seats['seats'])

				# Count the number of tickets purchased for the flight
				count_tickets_purchased = 'SELECT COUNT(ticket_ID) AS tickets_purchased FROM Customer_Purchases WHERE flight_num = %s'
				cursor.execute(count_tickets_purchased, (flight_purchase))
				tickets_purchased = cursor.fetchone()
				tickets_purchased = int(tickets_purchased['tickets_purchased'])

				# Determine the capacity of the flight by dividing the number of tickets purchased by the number of seats on the airplane
				capacity = (tickets_purchased / seats) * 100

				# If the capacity of the flight> 70, the sold price is 1.2 * base_price
				if(capacity > 70):
					sold_price = base_price * 1.2
				else:
					sold_price = base_price

				insert_purchase = 'INSERT INTO CUSTOMER_PURCHASES (cus_email, ticket_ID, flight_num, sold_price, card_type, card_num, card_name, card_exp_date, \
									purchase_date, purchase_time, agent_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, DATE(NOW()), TIME(NOW()), %s)'

				cursor.execute(insert_purchase, (cus_email, ticket_ID, flight_purchase, sold_price, card_type, card_num, card_name, card_exp, agent_ID))
				conn.commit()

		cursor.close()
		return render_template('agentHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, month_commission=month_commission, \
								month_tickets_sold=tickets_sold, month_comm_per_ticket=comm_per_ticket, top_customers_month=top_customers_month, \
								top_customers_year=top_customers_year, purchase="Complete")


	# When a customer clicks the "Search" button under 'My Spending', the program will determine how much money that customer spent between two user-specified dates (track_spending = True)
	if (track_commission == True):
		calc_commission = 'SELECT SUM(sold_price) AS commission, COUNT(ticket_ID) as tickets_sold FROM Customer_Purchases WHERE agent_ID = %s AND purchase_date >= %s AND purchase_date <= %s'
		cursor.execute(calc_commission, (agent_ID, start_date, end_date))
		commission_info = cursor.fetchone()
		commission = commission_info['commission']

		if (commission == None):
			commission='0.0'
			comm_per_ticket = '0.0'
			tickets_sold = 0
		else:
			commission = int(commission) * 0.1
			tickets_sold = int(commission_info['tickets_sold'])
			comm_per_ticket = commission / tickets_sold

		cursor.close()
		return render_template('agentHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, month_commission=commission, \
								month_tickets_sold=tickets_sold, month_comm_per_ticket=comm_per_ticket, top_customers_month=top_customers_month, \
								top_customers_year=top_customers_year, date_commission=commission, date_tickets_sold=tickets_sold, \
								date_comm_per_ticket=comm_per_ticket, start_date=start_date, end_date=end_date)

	# Returns default information that is displayed each time the page is loaded or refreshed
	cursor.close()
	return render_template('agentHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
							past_flights_info=past_flights_info, future_flights_info=future_flights_info, month_commission=commission, \
							month_tickets_sold=tickets_sold, month_comm_per_ticket=comm_per_ticket, top_customers_month=top_customers_month, \
							top_customers_year=top_customers_year)
		

	######################################################################THIS CODE RUNS EVERYTIME THE PAGE IS LOADED OR REFRESHED######################################################################


@app.route('/staffHome', methods=['GET', 'POST'])
def staffHome():
	username = session['username']

	conduct_flight_search = False
	if ('trip_type' in request.form and 'source' in request.form and 'destination' in request.form and 'departure' in request.form and 'arrival' in request.form):	
		conduct_flight_search = True
		trip_type = request.form['trip_type']
		source = request.form['source']
		destination = request.form['destination']	
		departure = request.form['departure']
		arrival = request.form['arrival']


	conduct_customer_search = False
	if ('customer_flight_select' in request.form):
		conduct_customer_search = True
		customer_flight_select = request.form['customer_flight_select']


	add_flight = False
	if ('airplane_ID' in request.form and 'trip_type' in request.form and 'departure_airport' in request.form and 'departure_date' in request.form \
		and 'departure_time' in request.form and 'arrival_airport' in request.form and 'arrival_date' in request.form and 'arrival_time' in request.form \
		and 'base_price' in request.form and 'flight_status' in request.form):

		add_flight = True
		airplane_ID = request.form['airplane_ID']
		trip_type = request.form['trip_type']
		departure_airport = request.form['departure_airport']
		departure_date = request.form['departure_date']
		departure_time = request.form['departure_time']
		arrival_airport = request.form['arrival_airport']
		arrival_date = request.form['arrival_date']
		arrival_time = request.form['arrival_time']
		base_price = request.form['base_price']
		flight_status = request.form['flight_status']


	change_flight_status = False
	if ('flight_select' in request.form and 'flight_status' in request.form):
		change_flight_status = True
		flight_select = request.form['flight_select']
		flight_status = request.form['flight_status']


	add_airplane = False
	if ('seats' in request.form):
		add_airplane = True
		seats = request.form['seats']


	add_airport = False
	if ('airport_name' in request.form and 'city' in request.form):
		add_airport = True
		airport_name = request.form['airport_name']
		city = request.form['city']


	view_flight_review = False
	if ('review_flight_select' in request.form):
		view_flight_review = True
		review_flight_select = request.form['review_flight_select']

	cursor = conn.cursor()

	staff_airline = 'SELECT airline_name FROM Airline_Staff WHERE staff_username = %s'
	cursor.execute(staff_airline, (username))
	airline_name = cursor.fetchone()
	airline_name = airline_name['airline_name']


	find_airplanes = 'SELECT * FROM Airplane WHERE airline_name = %s'
	cursor.execute(find_airplanes, (airline_name))
	airplanes = cursor.fetchall()
	# later: what if they have no airplanes?


	find_past_flights = 'SELECT * FROM Flight WHERE airline_name = %s AND departure_date >= DATE_SUB(DATE(NOW()), INTERVAL 30 DAY) AND departure_date <= DATE(NOW())'
	cursor.execute(find_past_flights, (airline_name))
	past_flights = cursor.fetchall()


	find_future_flights = 'SELECT * FROM Flight WHERE airline_name = %s AND departure_date >= DATE(NOW()) AND departure_date <= DATE_ADD(DATE(NOW()), INTERVAL 30 DAY)'
	cursor.execute(find_future_flights, (airline_name))
	future_flights = cursor.fetchall()


	find_top_agents = 'SELECT Customer_Purchases.agent_ID, SUM(purchase_ID) as purchases FROM Customer_Purchases, Booking_Agent WHERE \
						Customer_Purchases.agent_ID = Booking_Agent.agent_ID AND airline_name = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 MONTH) \
						GROUP BY agent_ID ORDER BY purchases DESC LIMIT 0, 5'
	cursor.execute(find_top_agents, (airline_name))
	top_agents_month = cursor.fetchall()
	print(top_agents_month)

	find_top_agents = 'SELECT Customer_Purchases.agent_ID, SUM(purchase_ID) as purchases FROM Customer_Purchases, Booking_Agent WHERE \
						Customer_Purchases.agent_ID = Booking_Agent.agent_ID AND airline_name = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 YEAR) \
						GROUP BY agent_ID ORDER BY purchases DESC LIMIT 0, 5'
	cursor.execute(find_top_agents, (airline_name))
	top_agents_year = cursor.fetchall()
	print(top_agents_year)

	find_top_agents = 'SELECT Customer_Purchases.agent_ID, SUM(sold_price) * 0.1 as commission FROM Customer_Purchases, Booking_Agent WHERE \
						Customer_Purchases.agent_ID = Booking_Agent.agent_ID AND airline_name = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 YEAR) \
						GROUP BY agent_ID ORDER BY commission DESC LIMIT 0, 5'
	cursor.execute(find_top_agents, (airline_name))
	top_agents_commission = cursor.fetchall()
	print(top_agents_commission)


	# When a customer clicks the "Search" button under 'Search for and Purchase Flights', a flight serarch will be conducted (conduct_flight_search = True)
	if (conduct_flight_search == True):
		search_flights = 'SELECT * FROM Flight WHERE departure_airport = %s AND arrival_airport = %s AND trip_type = %s AND departure_date >= %s AND arrival_date <= %s'				
		cursor.execute(search_flights, (source, destination, trip_type, departure, arrival))
		query_flights = cursor.fetchall()

		if (not query_flights):
			query_flights = "No Results"

		cursor.close()
		return render_template('staffHome.html', username=username, past_flights=past_flights, future_flights=future_flights, airplanes=airplanes, top_agents_month=top_agents_month, top_agents_year=top_agents_year, top_agents_commission=top_agents_commission, query_flights=query_flights)


	if (conduct_customer_search == True):
		search_flights = 'SELECT cus_email FROM Customer_Purchases WHERE flight_num = %s'				
		cursor.execute(search_flights, (customer_flight_select))
		customers = cursor.fetchall()

		if (not customers):
			customers = "No Results"

		cursor.close()
		return render_template('staffHome.html', username=username, past_flights=past_flights, future_flights=future_flights, airplanes=airplanes, top_agents_month=top_agents_month, top_agents_year=top_agents_year, top_agents_commission=top_agents_commission, customers=customers, customer_flight_select=customer_flight_select)


	if (add_flight == True):
		insert_flight = 'INSERT INTO Flight (airline_name, airplane_ID, departure_airport, departure_date, departure_time, \
						arrival_airport, arrival_date, arrival_time, base_price, flight_status, trip_type) \
						VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(insert_flight, (airline_name, airplane_ID, departure_airport, departure_date, departure_time, arrival_airport, arrival_date, arrival_time, base_price, flight_status, trip_type))
		conn.commit()
		cursor.close()
		# return render_template('staffHome.html', username=username, past_flights=past_flights, future_flights=future_flights, airplanes=airplanes, add_flight="Complete")
		return redirect(url_for('staffHome'))


	if (change_flight_status == True):
		update_flight = 'UPDATE Flight SET flight_status = %s WHERE flight_num = %s'
		cursor.execute(update_flight, (flight_status, flight_select))
		conn.commit()
		
		cursor.close()
		# return render_template('staffHome.html', username=username, past_flights=past_flights, future_flights=future_flights, airplanes=airplanes, change_flight_status="Complete", flight_selct=flight_select)
		return redirect(url_for('staffHome'))

	if (add_airplane == True):
		insert_airplane = 'INSERT INTO AIRPLANE (airline_name, seats) VALUES (%s, %s)'
		cursor.execute(insert_airplane, (airline_name, seats))
		conn.commit()
		
		cursor.close()
		# return render_template('staffHome.html', username=username, past_flights=past_flights, future_flights=future_flights, airplanes=airplanes, add_airplane="Complete")
		return redirect(url_for('staffConfirmation'))

	if (add_airport == True):
		insert_airport = 'INSERT INTO AIRPORT (airport_name, city) VALUES (%s, %s)'
		cursor.execute(insert_airport, (airport_name, city))
		conn.commit()
		
		cursor.close()
		return redirect(url_for('staffHome'))

	if (view_flight_review == True):
		find_flight_review = 'SELECT * FROM REVIEW WHERE flight_num = %s'
		cursor.execute(find_flight_review, (review_flight_select))
		reviews = cursor.fetchall()

		if (reviews == ()):
			reviews = "No Reviews"
		else:
			find_avg_rating = 'SELECT AVG(rating) as avg_rating FROM REVIEW WHERE flight_num = %s'
			cursor.execute(find_avg_rating, (review_flight_select))
			avg_rating = cursor.fetchone()
			avg_rating = avg_rating['avg_rating']
		
		cursor.close()
		return render_template('staffHome.html', username=username, past_flights=past_flights, future_flights=future_flights, airplanes=airplanes, top_agents_month=top_agents_month, top_agents_year=top_agents_year, top_agents_commission=top_agents_commission, reviews=reviews, avg_rating=avg_rating)

	cursor.close()
	return render_template('staffHome.html', username=username, past_flights=past_flights, future_flights=future_flights, airplanes=airplanes, top_agents_month=top_agents_month, top_agents_year=top_agents_year, top_agents_commission=top_agents_commission)


@app.route('/staffConfirmation')
def staffConfirmation():
	username = session['username']

	cursor = conn.cursor()

	staff_airline = 'SELECT airline_name FROM Airline_Staff WHERE staff_username = %s'
	cursor.execute(staff_airline, (username))
	airline_name = cursor.fetchone()
	airline_name = airline_name['airline_name']

	find_airplanes = 'SELECT * FROM Airplane WHERE airline_name = %s'
	cursor.execute(find_airplanes, (airline_name))
	airplanes = cursor.fetchall()

	cursor.close()

	return render_template('staffConfirmation.html', username=username, airplanes=airplanes)


@app.route('/customerLogout')
def customerLogout():
	session.pop('username')
	return redirect('/customerLogin')

@app.route('/agentLogout')
def agentLogout():
	session.pop('username')
	return redirect('/agentLogin')

@app.route('/staffLogout')
def staffLogout():
	session.pop('username')
	return redirect('/staffLogin')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 8888
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
