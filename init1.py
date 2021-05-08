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

	# Finds all airports that belong to the airline
	find_airports = 'SELECT * FROM airport'
	cursor.execute(find_airports)
	airports = cursor.fetchall()


	# Finds all airlines that belong to the airline
	find_airlines = 'SELECT * FROM airline'
	cursor.execute(find_airlines)
	airlines = cursor.fetchall()


	# Finds all flights that belong to the airline
	find_flights = 'SELECT * FROM Flight'
	cursor.execute(find_flights)
	flights = cursor.fetchall()


	# When a customer clicks the "Search" button under 'Search for and Purchase Flights', a flight search will be conducted (conduct_flight_search = True)
	if (conduct_flight_search == True):
		search_flights = 'SELECT * FROM Flight WHERE departure_airport = %s AND arrival_airport = %s AND trip_type = %s AND departure_date >= DATE(NOW()) AND arrival_date >= DATE(NOW()) AND departure_date >= %s AND arrival_date <= %s'				
		cursor.execute(search_flights, (source, destination, trip_type, departure, arrival))
		query_flights = cursor.fetchall()

		if (not query_flights):
			query_flights = "No Results"

		cursor.close()
		return render_template('index.html', airports=airports, airlines=airlines, flights=flights, query_flights=query_flights)


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
		return render_template('index.html', airports=airports, airlines=airlines, flights=flights, flight_num=flight_num, flight_status=flight_status)


	return render_template('index.html', airports=airports, airlines=airlines, flights=flights)

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


	# When a customer clicks the "Search" button under 'Search for and Purchase Flights', a flight search will be conducted (conduct_flight_search = True)
	# We know when a customer clicks this button if we recieve 'trip_type', 'source', 'destination', 'departure', and 'arrival' in the the 'POST' Form
	conduct_flight_search = False
	if ('trip_type' in request.form and 'source' in request.form and 'destination' in request.form and 'departure' in request.form and 'arrival' in request.form):	
		conduct_flight_search = True
		trip_type = request.form['trip_type']
		source = request.form['source']
		destination = request.form['destination']	
		departure = request.form['departure']
		arrival = request.form['arrival']


	# When a customer clicks the "Yes" button under 'Check Availability' for a certain flight, a ticket search will be conducted (conduct_ticket_search = True) for that flight.
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


	# Finds all airports that belong to the airline
	find_airports = 'SELECT * FROM airport'
	cursor.execute(find_airports)
	airports = cursor.fetchall()
	

	# When the page is loaded or refreshed, the program finds all flights that a customer has purchased from Customer_Purchases Table using their email
	find_flights = 'SELECT flight_num, ticket_ID, sold_price FROM Customer_Purchases WHERE cus_email = %s'
	cursor.execute(find_flights, (username))
	all_flights = cursor.fetchall()

	all_flights_info = []
	past_flights_info = []
	future_flights_info = []

	flightsOccured = []

	# When the page is loaded or refreshed, the program finds additional information about each flight that is not stored in the Cutomer_Purchases Table using the Flight Table
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


	# When the page is loaded or refreshed, the program calculates the customer's expenses within the past 6 months by finding the sum of the sold_prices for the tickets in the Customer_Purchases table using their email
	calc_six_month_expenses = 'SELECT SUM(sold_price) AS month_expense, MONTHNAME(purchase_date) AS month FROM Customer_Purchases WHERE cus_email = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 6 MONTH) GROUP BY month ORDER BY DATE(NOW())'
	cursor.execute(calc_six_month_expenses, (username))
	six_month_expenses = cursor.fetchall()

	if (six_month_expenses == None):
		six_month_expenses="0.0"
		
	######################################################################THIS CODE RUNS EVERYTIME THE PAGE IS LOADED OR REFRESHED######################################################################


	# When a customer clicks the "Search" button under 'Search for and Purchase Flights', a flight search will be conducted (conduct_flight_search = True)
	if (conduct_flight_search == True):
		search_flights = 'SELECT * FROM Flight WHERE departure_airport = %s AND arrival_airport = %s AND trip_type = %s AND departure_date >= DATE(NOW()) AND arrival_date >= DATE(NOW()) AND departure_date >= %s AND arrival_date <= %s'
		cursor.execute(search_flights, (source, destination, trip_type, departure, arrival))
		query_flights = cursor.fetchall()

		if (not query_flights):
			query_flights = "No Results"

		cursor.close()
		return render_template('customerHome.html', username=username, airports=airports, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, \
								year_expenses=year_expenses, six_month_expenses=six_month_expenses, \
								query_flights=query_flights)


	# When a customer clicks the "Yes" button under 'Check Availability' for a certain flight, a ticket search will be conducted (conduct_ticket_search = True) for that flight.
	# A purchase form will be revealed if there are tickets avaiable.
	if (conduct_ticket_search == True):
		search_tickets = 'SELECT ticket_ID FROM Ticket WHERE flight_num = %s AND is_purchased = "No"'
		cursor.execute(search_tickets, (flight_select))
		tickets = cursor.fetchall()

		if (not tickets):
			tickets = "No Tickets"

		cursor.close()
		return render_template('customerHome.html', username=username, airports=airports, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, \
								year_expenses=year_expenses, six_month_expenses=six_month_expenses, \
								flight_select=flight_select, tickets=tickets)


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
		return redirect(url_for('customerHome'))

	# When a customer clicks the "Yes" button under 'Rate and Review', a form will be revealed to the user under 'Review Previously Taken Flights' (reveal_review_form = True)
	# A customer who has already reviewed a flight will not be able to review it again
	if (reveal_review_form == True):
		search_reviews = 'SELECT * FROM Review WHERE flight_num = %s AND cus_email = %s'
		cursor.execute(search_reviews, (flight_to_rate, username))
		isFlightRated = cursor.fetchall()

		if (not isFlightRated):
			cursor.close()
			return render_template('customerHome.html', username=username, airports=airports, all_flights=all_flights, all_flights_info=all_flights_info, \
									past_flights_info=past_flights_info, future_flights_info=future_flights_info, \
									year_expenses=year_expenses, six_month_expenses=six_month_expenses, \
									flight_to_rate=flight_to_rate)
		else:
			cursor.close()
			return render_template('customerHome.html', username=username, airports=airports, all_flights=all_flights, all_flights_info=all_flights_info, \
									past_flights_info=past_flights_info, future_flights_info=future_flights_info, \
									year_expenses=year_expenses, six_month_expenses=six_month_expenses, \
									flight_rated=flight_to_rate, review="Already Complete")


	# When a customer clicks the "Submit" button under 'Review Previously Taken Flights', their review will be submitted (submit_rating = True)
	if (submit_rating == True):
		submit_flight_rating = 'INSERT INTO Review(cus_email, flight_num, rating, comment) VALUES(%s, %s, %s, %s)'
		cursor.execute(submit_flight_rating, (username, flight_rated, rating, comment))
		conn.commit()

		cursor.close()
		return redirect(url_for('customerHome'))

	
	# When a customer clicks the "Search" button under 'My Spending', the program will determine how much money that customer spent between two user-specified dates (track_spending = True)
	if (track_spending == True):
		calc_date_expenses = 'SELECT SUM(sold_price) AS date_expenses FROM Customer_Purchases WHERE cus_email = %s AND purchase_date >= %s AND purchase_date <= %s'
		cursor.execute(calc_date_expenses, (username, start_date, end_date))
		date_expenses = cursor.fetchone()
		date_expenses = date_expenses['date_expenses']

		if (date_expenses == None):
			date_expenses="0.0"

		calc_range_month_expenses = 'SELECT SUM(sold_price) AS month_expense, MONTHNAME(purchase_date) AS month FROM Customer_Purchases WHERE cus_email = %s AND purchase_date >= %s AND purchase_date <= %s GROUP BY month ORDER BY DATE(NOW())'
		cursor.execute(calc_range_month_expenses, (username, start_date, end_date))
		range_month_expenses = cursor.fetchall()

		if (range_month_expenses == None):
			range_month_expenses="0.0"

		cursor.close()
		return render_template('customerHome.html', username=username, airports=airports, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, \
								year_expenses=year_expenses, six_month_expenses=six_month_expenses, \
								date_expenses=date_expenses, range_month_expenses=range_month_expenses, start_date=start_date, end_date=end_date)


	# Returns default information that is displayed each time the page is loaded or refreshed
	cursor.close()
	return render_template('customerHome.html', username=username, airports=airports, all_flights=all_flights, all_flights_info=all_flights_info, \
							past_flights_info=past_flights_info, future_flights_info=future_flights_info, \
							year_expenses=year_expenses, six_month_expenses=six_month_expenses)


@app.route('/agentHome', methods=['GET', 'POST'])
def agentHome():
	username = session['username']

	# When a booking agent clicks the "Search" button under 'Search for and Purchase Flights', a flight search will be conducted (conduct_flight_search = True)
	# We know when a booking agent clicks this button if we recieve 'trip_type', 'source', 'destination', 'departure', and 'arrival' in the the 'POST' Form
	conduct_flight_search = False
	if ('trip_type' in request.form and 'source' in request.form and 'destination' in request.form and 'departure' in request.form and 'arrival' in request.form):	
		conduct_flight_search = True
		trip_type = request.form['trip_type']
		source = request.form['source']
		destination = request.form['destination']	
		departure = request.form['departure']
		arrival = request.form['arrival']


	# When a booking agent clicks the "Yes" button under 'Check Availability' for a certain flight, a ticket search will be conducted (conduct_ticket_search = True) for that flight.
	# A purchase form will be revealed if there are tickets avaiable.
	# We know when a booking agent clicks this button if we recieve 'flight_select' in the the 'POST' Form
	conduct_ticket_search = False
	if ('flight_select' in request.form):
		conduct_ticket_search = True
		flight_select = request.form['flight_select']


	# When a booking agent clicks the "Purchase" button under 'Purchase Tickets', a ticket purchase will be conducted (conduct_ticket_purchase = True)
	# We know when a booking agent clicks this button if we recieve 'flight_purchase', 'ticket', 'type', 'num', 'name', and 'exp' in the the 'POST' Form
	conduct_ticket_purchase = False
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
	track_commission = False
	if ('start_date' in request.form and 'end_date' in request.form):	
		track_commission = True
		start_date = request.form['start_date']
		end_date = request.form['end_date']


	######################################################################THIS CODE RUNS EVERYTIME THE PAGE IS LOADED OR REFRESHED######################################################################

	# establish connection with PHPMyAdmin
	cursor = conn.cursor()

	# Finds all airports that belong to the airline
	find_airports = 'SELECT * FROM airport'
	cursor.execute(find_airports)
	airports = cursor.fetchall()
	

	# When the page is loaded or refreshed, the program finds the agent_ID of the booking agent using their email in the Customer_Purchases Table
	find_agent_ID = 'SELECT agent_ID FROM Booking_Agent WHERE agent_email = %s'
	cursor.execute(find_agent_ID, (username))
	agent_ID = cursor.fetchone()
	agent_ID = agent_ID['agent_ID']	


	# When the page is loaded or refreshed, the program finds all flights that a booking agent has purchased from Customer_Purchases Table using their agent_ID
	find_flights = 'SELECT cus_email, flight_num, ticket_ID FROM Customer_Purchases WHERE agent_ID = %s'
	cursor.execute(find_flights, (agent_ID))
	all_flights = cursor.fetchall()

	all_flights_info = []
	past_flights_info = []
	future_flights_info = []

	flightsOccured = []

	# When the page is loaded or refreshed, the program finds additional information about each flight that isn't stored in the Cutomer_Purchases Table using the Flight Table
	for flight in all_flights:

		# Prevents duplicate flight information from being selected
		if (flight['flight_num'] not in flightsOccured):

			find_all_flights_info = 'SELECT * FROM Flight WHERE flight_num = %s'

			cursor.execute(find_all_flights_info, (flight['flight_num']))
			flight_info = cursor.fetchone()
			all_flights_info.append(flight_info)

			flightsOccured.append(flight['flight_num'])


	# When the page is loaded or refreshed, the program finds additional information about each PAST flight that isn't stored in the Cutomer_Purchases Table using the Flight Table
	flightsOccured = []
	for flight in all_flights:

		# Prevents duplicate flight information from being selected
		if (flight['flight_num'] not in flightsOccured):

			find_past_flights_info = 'SELECT * FROM Flight WHERE flight_num = %s AND departure_date < DATE(NOW())'

			cursor.execute(find_past_flights_info, (flight['flight_num']))
			flight_info = cursor.fetchone()
			past_flights_info.append(flight_info)

			flightsOccured.append(flight['flight_num'])


	# When the page is loaded or refreshed, the program finds additional information about each FUTURE flight that isn't stored in the Cutomer_Purchases Table using the Flight Table
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

	find_customers = 'SELECT cus_email, COUNT(ticket_ID) as tickets FROM Customer_Purchases WHERE agent_ID = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 6 MONTH) GROUP BY cus_email ORDER BY tickets DESC LIMIT 0, 5'
	cursor.execute(find_customers, (agent_ID))
	top_customers_month = cursor.fetchall()

	find_customers = 'SELECT cus_email, SUM(sold_price) * 0.1 as cus_commission FROM Customer_Purchases WHERE agent_ID = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 YEAR) GROUP BY cus_email ORDER BY cus_commission DESC LIMIT 0, 5'
	cursor.execute(find_customers, (agent_ID))
	top_customers_year = cursor.fetchall()


	######################################################################THIS CODE RUNS EVERYTIME THE PAGE IS LOADED OR REFRESHED######################################################################


	# When a customer clicks the "Search" button under 'Search for and Purchase Flights', a flight search will be conducted (conduct_flight_search = True)
	if (conduct_flight_search == True):
		search_flights = 'SELECT * FROM Flight WHERE departure_airport = %s AND arrival_airport = %s AND trip_type = %s AND departure_date >= DATE(NOW()) AND arrival_date >= DATE(NOW()) AND departure_date >= %s AND arrival_date <= %s'				
		cursor.execute(search_flights, (source, destination, trip_type, departure, arrival))
		query_flights = cursor.fetchall()

		if (not query_flights):
			query_flights = "No Results"

		cursor.close()
		return render_template('agentHome.html', username=username, airports=airports, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, \
								month_commission=commission, month_tickets_sold=tickets_sold, month_comm_per_ticket=comm_per_ticket, \
								top_customers_month=top_customers_month, top_customers_year=top_customers_year, \
								query_flights=query_flights)


	# When a booking agent clicks the "Yes" button under 'Check Availability' for a certain flight, a ticket search will be conducted (conduct_ticket_search = True) for that flight.
	# A purchase form will be revealed if there are tickets avaiable.
	if (conduct_ticket_search == True):
		search_tickets = 'SELECT ticket_ID FROM Ticket WHERE flight_num = %s AND is_purchased = "No"'
		cursor.execute(search_tickets, (flight_select))
		tickets = cursor.fetchall()

		if (not tickets):
			tickets = "No Tickets"

		cursor.close()
		return render_template('agentHome.html', username=username, airports=airports, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, \
								month_commission=commission, month_tickets_sold=tickets_sold, month_comm_per_ticket=comm_per_ticket, \
								top_customers_month=top_customers_month, top_customers_year=top_customers_year, \
								flight_select=flight_select, tickets=tickets)


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
		return redirect(url_for('agentHome'))


	# When a customer clicks the "Search" button under 'My Spending', the program will determine how much money that customer spent between two user-specified dates (track_spending = True)
	if (track_commission == True):
		calc_commission = 'SELECT SUM(sold_price) AS commission, COUNT(ticket_ID) as tickets_sold FROM Customer_Purchases WHERE agent_ID = %s AND purchase_date >= %s AND purchase_date <= %s'
		cursor.execute(calc_commission, (agent_ID, start_date, end_date))
		commission_info = cursor.fetchone()
		date_commission = commission_info['commission']

		if (date_commission == None):
			date_commission='0.0'
			date_comm_per_ticket = '0.0'
			date_tickets_sold = 0
		else:
			date_commission = int(date_commission) * 0.1
			date_tickets_sold = int(commission_info['tickets_sold'])
			date_comm_per_ticket = date_commission / date_tickets_sold

		cursor.close()
		return render_template('agentHome.html', username=username, airports=airports, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, \
								month_commission=commission, month_tickets_sold=tickets_sold, month_comm_per_ticket=comm_per_ticket, \
								top_customers_month=top_customers_month, top_customers_year=top_customers_year, \
								date_commission=date_commission, date_tickets_sold=date_tickets_sold, date_comm_per_ticket=date_comm_per_ticket, start_date=start_date, end_date=end_date)


	# Returns default information that is displayed each time the page is loaded or refreshed
	cursor.close()
	return render_template('agentHome.html', username=username, airports=airports, all_flights=all_flights, all_flights_info=all_flights_info, \
							past_flights_info=past_flights_info, future_flights_info=future_flights_info, \
							month_commission=commission, month_tickets_sold=tickets_sold, month_comm_per_ticket=comm_per_ticket, \
							top_customers_month=top_customers_month, top_customers_year=top_customers_year)
		

	######################################################################THIS CODE RUNS EVERYTIME THE PAGE IS LOADED OR REFRESHED######################################################################


@app.route('/staffHome', methods=['GET', 'POST'])
def staffHome():
	username = session['username']


	# When an airline staff member clicks the "Search" button under 'Search for Flights', a flight search will be conducted (conduct_flight_search = True)
	# We know when an airline staff member clicks this button if we recieve 'trip_type', 'source', 'destination', 'departure', and 'arrival' in the the 'POST' Form
	conduct_flight_search = False
	if ('trip_type' in request.form and 'source' in request.form and 'destination' in request.form and 'departure' in request.form and 'arrival' in request.form):	
		conduct_flight_search = True
		trip_type = request.form['trip_type']
		source = request.form['source']
		destination = request.form['destination']	
		departure = request.form['departure']
		arrival = request.form['arrival']


	# After an airline staff member searches for flights, they can click the "Yes" button under 'View Customers' to view the customers who have purchased a ticket for that flight.
	# We know when an airline staff member clicks this button if we recieve 'customer_flight_select' (i.e the flight that had been specified) in the the 'POST' Form
	conduct_customer_search = False
	if ('customer_flight_select' in request.form):
		conduct_customer_search = True
		customer_flight_select = request.form['customer_flight_select']


	# When an airline staff member clicks the "Add Flight" button under 'Add New Flight', a flight will be added (add_flight = True)
	# We know when an airline staff member clicks this button if we recieve 'airplane_ID', 'trip_type', 'departure_airport', etc. in the the 'POST' Form
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


	# When an airline staff member clicks the "Change Flight Status" button under 'Future Flights (30 Days)', the flight status will be changed (change_flight_status = True)
	# We know when an airline staff member clicks this button if we recieve 'flight_select' and 'flight_status' in the the 'POST' Form
	change_flight_status = False
	if ('flight_select' in request.form and 'flight_status' in request.form):
		change_flight_status = True
		flight_select = request.form['flight_select']
		flight_status = request.form['flight_status']


	# When an airline staff member clicks the "Add Airplane" button under 'Add New Airplane', an airplane will be added (add_airplane = True)
	# We know when an airline staff member clicks this button if we recieve 'seats' in the the 'POST' Form
	add_airplane = False
	if ('seats' in request.form):
		add_airplane = True
		seats = request.form['seats']


	# When an airline staff member clicks the "Add Airport" button under 'Add New Airport', an airport will be added (add_airport = True)
	# We know when an airline staff member clicks this button if we recieve 'airport_name' and 'city' in the the 'POST' Form
	add_airport = False
	if ('airport_name' in request.form and 'city' in request.form):
		add_airport = True
		airport_name = request.form['airport_name']
		city = request.form['city']


	# After an airline staff member searches for flights, they can click the "Yes" button under 'View Ratings and Reviews', to find the flights avergae rating and all ratings/reviews
	# We know when an airline staff member clicks this button if we recieve 'review_flight_select' in the the 'POST' Form
	view_flight_review = False
	if ('review_flight_select' in request.form):
		view_flight_review = True
		review_flight_select = request.form['review_flight_select']


	# When an airline staff member clicks the "Find Customer's Flights" button under 'Find Customer Flights', all flights that a customer has purchased tickets for will be found
	# We know when an airline staff member clicks this button if we recieve 'cus_email' in the the 'POST' Form
	view_customer_flights = False
	if ('cus_email' in request.form):
		view_customer_flights = True
		cus_email = request.form['cus_email']


	# When an airline staff member clicks the "Find Tickets Sold" button under 'View Tickets Sold', all tickets purchased between two specified dates will be found.
	# We know when an airline staff member clicks this button if we recieve 'cus_email' in the the 'POST' Form
	view_tickets_sold = False
	if ('ticket_start_date' in request.form and 'ticket_end_date' in request.form):
		view_tickets_sold = True
		ticket_start_date = request.form['ticket_start_date']
		ticket_end_date = request.form['ticket_end_date']


	######################################################################THIS CODE RUNS EVERYTIME THE PAGE IS LOADED OR REFRESHED######################################################################


	cursor = conn.cursor()

	# Finds all airports that belong to the airline
	find_airports = 'SELECT * FROM airport'
	cursor.execute(find_airports)
	airports = cursor.fetchall()


	# Finds the airline that the airline staff member works for
	staff_airline = 'SELECT airline_name FROM Airline_Staff WHERE staff_username = %s'
	cursor.execute(staff_airline, (username))
	airline_name = cursor.fetchone()
	airline_name = airline_name['airline_name']


	# Finds all airplanes that belong to the airline
	find_airplanes = 'SELECT * FROM Airplane WHERE airline_name = %s'
	cursor.execute(find_airplanes, (airline_name))
	airplanes = cursor.fetchall()
	# later: what if they have no airplanes?


	# Finds flights that have departed within the past 30 days
	find_past_flights = 'SELECT * FROM Flight WHERE airline_name = %s AND departure_date >= DATE_SUB(DATE(NOW()), INTERVAL 30 DAY) AND departure_date <= DATE(NOW())'
	cursor.execute(find_past_flights, (airline_name))
	past_flights = cursor.fetchall()


	# Finds flights that will depart within the next 30 days
	find_future_flights = 'SELECT * FROM Flight WHERE airline_name = %s AND departure_date >= DATE(NOW()) AND departure_date <= DATE_ADD(DATE(NOW()), INTERVAL 30 DAY)'
	cursor.execute(find_future_flights, (airline_name))
	future_flights = cursor.fetchall()


	# Finds the top 5 booking agents based on how many tickets that they have sold within the past month using the Customer_purchases Table
	find_top_agents = 'SELECT Customer_Purchases.agent_ID, COUNT(purchase_ID) AS purchases FROM Customer_Purchases, Booking_Agent WHERE \
					   Customer_Purchases.agent_ID = Booking_Agent.agent_ID AND Booking_Agent.airline_name = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 MONTH) \
					   GROUP BY agent_ID ORDER BY purchases DESC LIMIT 0, 5'
	cursor.execute(find_top_agents, (airline_name))
	top_agents_month = cursor.fetchall()


	# Finds the top 5 booking agents based on how many tickets that they have sold within the past year using the Customer_Purchases Table
	find_top_agents = 'SELECT Customer_Purchases.agent_ID, COUNT(purchase_ID) AS purchases FROM Customer_Purchases, Booking_Agent WHERE \
					   Customer_Purchases.agent_ID = Booking_Agent.agent_ID AND Booking_Agent.airline_name = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 YEAR) \
					   GROUP BY agent_ID ORDER BY purchases DESC LIMIT 0, 5'
	cursor.execute(find_top_agents, (airline_name))
	top_agents_year = cursor.fetchall()


	# Finds the top 5 booking agents based on how much commission they earened within the past year using the Customer_Purchases and booking_Agent Table
	find_top_agents = 'SELECT Customer_Purchases.agent_ID, SUM(sold_price) * 0.1 AS commission FROM Customer_Purchases, Booking_Agent WHERE \
					   Customer_Purchases.agent_ID = Booking_Agent.agent_ID AND Booking_Agent.airline_name = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 YEAR) \
					   GROUP BY agent_ID ORDER BY commission DESC LIMIT 0, 5'
	cursor.execute(find_top_agents, (airline_name))
	top_agents_commission = cursor.fetchall()


	# Finds the most frequent customer within the past year based on how many tickets they have purchased using the Customer_Purchases and Flight Table
	find_customers = 'SELECT cus_email, COUNT(purchase_ID) AS purchases FROM Customer_Purchases, Flight WHERE Customer_Purchases.flight_num = Flight.flight_num \
					  AND Flight.airline_name = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 YEAR) GROUP BY cus_email ORDER BY purchases DESC LIMIT 0, 1'
	cursor.execute(find_customers, (airline_name))
	top_customer = cursor.fetchone()


	# Finds the number of tickets told within the past month using the Customer_Purchases and Flight Table
	find_tickets_sold = 'SELECT COUNT(ticket_ID) AS tickets_sold from Customer_Purchases, Flight WHERE Customer_Purchases.flight_num = Flight.flight_num \
						 AND Flight.airline_name = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 MONTH)'
	cursor.execute(find_tickets_sold, (airline_name))
	tickets_sold_month = cursor.fetchone()
	tickets_sold_month = tickets_sold_month['tickets_sold']

	if (not tickets_sold_month):
		tickets_sold_month = 0


	# Finds the number of tickets told within the past year using the Customer_Purchases and Flight Table
	find_tickets_sold = 'SELECT COUNT(ticket_ID) AS tickets_sold from Customer_Purchases, Flight WHERE Customer_Purchases.flight_num = Flight.flight_num \
						 AND Flight.airline_name = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 YEAR)'
	cursor.execute(find_tickets_sold, (airline_name))
	tickets_sold_year = cursor.fetchone()
	tickets_sold_year = tickets_sold_year['tickets_sold']

	if (not tickets_sold_year):
		tickets_sold_year = 0


	# Finds the number of tickets told within the past year, BY MONTH, using the Customer_Purchases and Flight Table
	find_tickets_sold = 'SELECT COUNT(ticket_ID) AS tickets_sold, MONTHNAME(purchase_date) AS month FROM Customer_Purchases, Flight WHERE Customer_Purchases.flight_num = Flight.flight_num \
						 AND Flight.airline_name = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 YEAR) GROUP BY month ORDER BY DATE(NOW())'
	cursor.execute(find_tickets_sold, (airline_name))
	tickets_sold_yearly_graph = cursor.fetchall()

	if (tickets_sold_yearly_graph == ()):
		tickets_sold_yearly_graph = "No Tickets Sold"


	# Finds the total amount of revenue earned from direct sales (customer bought tickets without booking agent) within the past month using the Customer_Purchases and Flight Table
	find_direct_revenue_month = 'SELECT SUM(sold_price) AS direct_revenue from Customer_Purchases, Flight WHERE Customer_Purchases.flight_num = Flight.flight_num \
								 AND Flight.airline_name = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 MONTH) AND agent_ID IS NULL'
	cursor.execute(find_direct_revenue_month, (airline_name))
	direct_revenue_month = cursor.fetchone()
	direct_revenue_month = direct_revenue_month['direct_revenue']

	if (direct_revenue_month == None):
		direct_revenue_month = 0.0


	# Finds the total amount of revenue earned from direct sales (customer bought tickets without booking agent) within the past year using the Customer_Purchases and Flight Table
	find_direct_revenue_year = 'SELECT SUM(sold_price) AS direct_revenue from Customer_Purchases, Flight WHERE Customer_Purchases.flight_num = Flight.flight_num \
								AND Flight.airline_name = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 YEAR) AND agent_ID IS NULL '
	cursor.execute(find_direct_revenue_year, (airline_name))
	direct_revenue_year = cursor.fetchone()
	direct_revenue_year = direct_revenue_year['direct_revenue']

	if (direct_revenue_year == None):
		direct_revenue_year = 0.0
		

	# Finds the total amount of revenue earned from indirect sales (customer bought tickets with booking agent) within the past month using the Customer_Purchases and Flight Table
	find_indirect_revenue_month = 'SELECT SUM(sold_price) AS indirect_revenue from Customer_Purchases, Flight WHERE Customer_Purchases.flight_num = Flight.flight_num \
								   AND Flight.airline_name = %s  AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 MONTH) AND agent_ID IS NOT NULL'
	cursor.execute(find_indirect_revenue_month, (airline_name))
	indirect_revenue_month = cursor.fetchone()
	indirect_revenue_month = indirect_revenue_month['indirect_revenue']

	if (indirect_revenue_month == None):
		indirect_revenue_month = 0.0


	# Finds the total amount of revenue earned from indirect sales (customer bought tickets with booking agent) within the past year using the Customer_Purchases and Flight Table
	find_indirect_revenue_year = 'SELECT SUM(sold_price) AS indirect_revenue from Customer_Purchases, Flight WHERE Customer_Purchases.flight_num = Flight.flight_num \
								  AND Flight.airline_name = %s  AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 YEAR) AND agent_ID IS NOT NULL'
	cursor.execute(find_indirect_revenue_year, (airline_name))
	indirect_revenue_year = cursor.fetchone()
	indirect_revenue_year = indirect_revenue_year['indirect_revenue']

	if (indirect_revenue_year == None):
		indirect_revenue_year = 0.0

	
	# Finds the top 3 destinations within last 3 months (based on tickets already sold) using the Customer_Purchases and Flight Table
	find_top_destinations_month = 'SELECT Flight.arrival_airport, COUNT(Flight.arrival_airport) AS tickets FROM Flight, Customer_Purchases WHERE \
								   Flight.flight_num = Customer_Purchases.flight_num AND Flight.airline_name = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 3 MONTH) \
								   GROUP BY Flight.arrival_airport ORDER BY tickets DESC LIMIT 0, 3'
	cursor.execute(find_top_destinations_month, (airline_name))
	top_destinations_month = cursor.fetchall()


	# Finds the top 3 destinations within past year (based on tickets already sold) using the Customer_Purchases and Flight Table
	find_top_destinations_year = 'SELECT Flight.arrival_airport, COUNT(Flight.arrival_airport) AS tickets FROM Flight, Customer_Purchases WHERE \
								  Flight.flight_num = Customer_Purchases.flight_num AND Flight.airline_name = %s AND purchase_date >= DATE_SUB(DATE(NOW()), INTERVAL 1 YEAR) \
								  GROUP BY Flight.arrival_airport ORDER BY tickets DESC LIMIT 0, 3'
	cursor.execute(find_top_destinations_year, (airline_name))
	top_destinations_year = cursor.fetchall()


	######################################################################THIS CODE RUNS EVERYTIME THE PAGE IS LOADED OR REFRESHED######################################################################


	# When a customer clicks the "Search" button under 'Search for Flights', a flight search will be conducted (conduct_flight_search = True)
	if (conduct_flight_search == True):
		search_flights = 'SELECT * FROM Flight WHERE departure_airport = %s AND arrival_airport = %s AND trip_type = %s AND departure_date >= DATE(NOW()) AND arrival_date >= DATE(NOW()) AND departure_date >= %s AND arrival_date <= %s'				
		cursor.execute(search_flights, (source, destination, trip_type, departure, arrival))
		query_flights = cursor.fetchall()

		if (not query_flights):
			query_flights = "No Results"

		cursor.close()
		return render_template('staffHome.html', username=username, airports=airports, past_flights=past_flights, future_flights=future_flights, airplanes=airplanes, \
								top_agents_month=top_agents_month, top_agents_year=top_agents_year, top_agents_commission=top_agents_commission, \
								top_customer=top_customer, tickets_sold_month=tickets_sold_month, tickets_sold_year=tickets_sold_year, tickets_sold_yearly_graph=tickets_sold_yearly_graph, \
								direct_revenue_month=direct_revenue_month, direct_revenue_year=direct_revenue_year, \
								indirect_revenue_month=indirect_revenue_month, indirect_revenue_year=indirect_revenue_year, \
								top_destinations_month=top_destinations_month, top_destinations_year=top_destinations_year, \
								query_flights=query_flights)


	# After an airline staff member searches for flights, they can click the "Yes" button under 'View Customers' to view the customers who have purchased a ticket for that flight.
	if (conduct_customer_search == True):
		search_flights = 'SELECT cus_email FROM Customer_Purchases WHERE flight_num = %s'				
		cursor.execute(search_flights, (customer_flight_select))
		customers = cursor.fetchall()

		if (not customers):
			customers = "No Results"

		cursor.close()
		return render_template('staffHome.html', username=username, airports=airports, past_flights=past_flights, future_flights=future_flights, airplanes=airplanes, \
								top_agents_month=top_agents_month, top_agents_year=top_agents_year, top_agents_commission=top_agents_commission, \
								top_customer=top_customer, tickets_sold_month=tickets_sold_month, tickets_sold_year=tickets_sold_year, tickets_sold_yearly_graph=tickets_sold_yearly_graph, \
								direct_revenue_month=direct_revenue_month, direct_revenue_year=direct_revenue_year, \
								indirect_revenue_month=indirect_revenue_month, indirect_revenue_year=indirect_revenue_year, \
								top_destinations_month=top_destinations_month, top_destinations_year=top_destinations_year, \
								customers=customers, customer_flight_select=customer_flight_select)


	# When an airline staff member clicks the "Add Flight" button under 'Add New Flight', a flight will be added (add_flight = True)
	if (add_flight == True):
		insert_flight = 'INSERT INTO Flight (airline_name, airplane_ID, departure_airport, departure_date, departure_time, \
						 arrival_airport, arrival_date, arrival_time, base_price, flight_status, trip_type) \
						 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(insert_flight, (airline_name, airplane_ID, departure_airport, departure_date, departure_time, arrival_airport, arrival_date, arrival_time, base_price, flight_status, trip_type))
		conn.commit()
		cursor.close()
		return redirect(url_for('staffHome'))


	# When an airline staff member clicks the "Change Flight Status" button under 'Future Flights (30 Days)', the flight status will be changed (change_flight_status = True)
	if (change_flight_status == True):
		update_flight = 'UPDATE Flight SET flight_status = %s WHERE flight_num = %s'
		cursor.execute(update_flight, (flight_status, flight_select))
		conn.commit()
		
		cursor.close()
		return redirect(url_for('staffHome'))


	# When an airline staff member clicks the "Add Airplane" button under 'Add New Airplane', an airplane will be added (add_airplane = True)
	if (add_airplane == True):
		insert_airplane = 'INSERT INTO AIRPLANE (airline_name, seats) VALUES (%s, %s)'
		cursor.execute(insert_airplane, (airline_name, seats))
		conn.commit()
		
		cursor.close()
		return redirect(url_for('staffConfirmation'))


	# When an airline staff member clicks the "Add Airport" button under 'Add New Airport', an airport will be added (add_airport = True)
	if (add_airport == True):
		insert_airport = 'INSERT INTO AIRPORT (airport_name, city) VALUES (%s, %s)'
		cursor.execute(insert_airport, (airport_name, city))
		conn.commit()
		
		cursor.close()
		return redirect(url_for('staffHome'))


	# After an airline staff member searches for flights, they can click the "Yes" button under 'View Ratings and Reviews', to find the flights avergae rating and all ratings/reviews
	if (view_flight_review == True):
		find_flight_review = 'SELECT * FROM REVIEW WHERE flight_num = %s'
		cursor.execute(find_flight_review, (review_flight_select))
		reviews = cursor.fetchall()

		if (reviews == ()):
			reviews = "No Reviews"
			avg_rating = 0
		else:
			find_avg_rating = 'SELECT AVG(rating) as avg_rating FROM REVIEW WHERE flight_num = %s'
			cursor.execute(find_avg_rating, (review_flight_select))
			avg_rating = cursor.fetchone()
			avg_rating = avg_rating['avg_rating']
		
		cursor.close()
		return render_template('staffHome.html', username=username, airports=airports, past_flights=past_flights, future_flights=future_flights, airplanes=airplanes, \
								top_agents_month=top_agents_month, top_agents_year=top_agents_year, top_agents_commission=top_agents_commission, \
								top_customer=top_customer, tickets_sold_month=tickets_sold_month, tickets_sold_year=tickets_sold_year, tickets_sold_yearly_graph=tickets_sold_yearly_graph, \
								direct_revenue_month=direct_revenue_month, direct_revenue_year=direct_revenue_year, \
								indirect_revenue_month=indirect_revenue_month, indirect_revenue_year=indirect_revenue_year, \
								top_destinations_month=top_destinations_month, top_destinations_year=top_destinations_year, \
								reviews=reviews, avg_rating=avg_rating)


	# When an airline staff member clicks the "Find Customer's Flights" button under 'Find Customer Flights', all flights that a customer has purchased tickets for will be found
	if (view_customer_flights == True):
		find_customer_flights = 'SELECT Customer_Purchases.flight_num FROM Customer_Purchases, Flight WHERE cus_email = %s AND Customer_Purchases.flight_num = Flight.flight_num \
								 AND Flight.airline_name = %s'
		cursor.execute(find_customer_flights, (cus_email, airline_name))
		customer_flights = cursor.fetchall()

		if (customer_flights == ()):
			customer_flights = "No Results"
		
		cursor.close()
		return render_template('staffHome.html', username=username, airports=airports, past_flights=past_flights, future_flights=future_flights, airplanes=airplanes, \
								top_agents_month=top_agents_month, top_agents_year=top_agents_year, top_agents_commission=top_agents_commission, \
								top_customer=top_customer, tickets_sold_month=tickets_sold_month, tickets_sold_year=tickets_sold_year, tickets_sold_yearly_graph=tickets_sold_yearly_graph, \
								direct_revenue_month=direct_revenue_month, direct_revenue_year=direct_revenue_year, \
								indirect_revenue_month=indirect_revenue_month, indirect_revenue_year=indirect_revenue_year, \
								top_destinations_month=top_destinations_month, top_destinations_year=top_destinations_year, \
								customer_flights=customer_flights)


	# When an airline staff member clicks the "Find Tickets Sold" button under 'View Tickets Sold', all tickets purchased between two specified dates will be found.
	if (view_tickets_sold == True):
		find_tickets_sold = 'SELECT COUNT(ticket_ID) as tickets_sold from Customer_Purchases, Flight WHERE Customer_Purchases.flight_num = Flight.flight_num \
							 AND Flight.airline_name = %s AND purchase_date >= %s AND purchase_date <= %s'
		cursor.execute(find_tickets_sold, (airline_name, ticket_start_date, ticket_end_date))
		tickets_sold = cursor.fetchone()
		tickets_sold = tickets_sold['tickets_sold']

		if (not tickets_sold):
			tickets_sold = 0

		# When an airline staff member clicks the "Find Tickets Sold" button under 'View Tickets Sold', all tickets purchased between two specified dates will be found, ordered BY MONTH.
		find_tickets_sold = 'SELECT COUNT(ticket_ID) AS tickets_sold, MONTHNAME(purchase_date) AS month FROM Customer_Purchases, Flight WHERE Customer_Purchases.flight_num = Flight.flight_num \
							AND Flight.airline_name = %s AND purchase_date >= %s AND purchase_date <= %s GROUP BY month ORDER BY DATE(NOW())'
		cursor.execute(find_tickets_sold, (airline_name, ticket_start_date, ticket_end_date))
		tickets_sold_range_graph = cursor.fetchall()

		if (tickets_sold_range_graph == ()):
			tickets_sold_range_graph = "No Tickets Sold"
		
		cursor.close()
		return render_template('staffHome.html', username=username, airports=airports, past_flights=past_flights, future_flights=future_flights, airplanes=airplanes, \
								top_agents_month=top_agents_month, top_agents_year=top_agents_year, top_agents_commission=top_agents_commission, \
								top_customer=top_customer, tickets_sold_month=tickets_sold_month, tickets_sold_year=tickets_sold_year, tickets_sold_yearly_graph=tickets_sold_yearly_graph, \
								direct_revenue_month=direct_revenue_month, direct_revenue_year=direct_revenue_year, \
								indirect_revenue_month=indirect_revenue_month, indirect_revenue_year=indirect_revenue_year, \
								top_destinations_month=top_destinations_month, top_destinations_year=top_destinations_year, \
								tickets_sold=tickets_sold, ticket_start_date=ticket_start_date, ticket_end_date=ticket_end_date, tickets_sold_range_graph=tickets_sold_range_graph)


	cursor.close()
	return render_template('staffHome.html', username=username, airports=airports, past_flights=past_flights, future_flights=future_flights, airplanes=airplanes, \
							top_agents_month=top_agents_month, top_agents_year=top_agents_year, top_agents_commission=top_agents_commission, \
							top_customer=top_customer, tickets_sold_month=tickets_sold_month, tickets_sold_year=tickets_sold_year, tickets_sold_yearly_graph=tickets_sold_yearly_graph, \
							direct_revenue_month=direct_revenue_month, direct_revenue_year=direct_revenue_year, \
							indirect_revenue_month=indirect_revenue_month, indirect_revenue_year=indirect_revenue_year, \
							top_destinations_month=top_destinations_month, top_destinations_year=top_destinations_year)


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
