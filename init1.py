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
                       db='AirTicketReservationSystem',
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
		search_flights = 'SELECT * FROM Flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_date = %s AND arrival_date = %s AND trip_type = %s AND departure_date >= DATE(NOW()) AND arrival_date >= DATE(NOW())'
						
		cursor.execute(search_flights, (source, destination, departure, arrival, trip_type))
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
	query = 'SELECT * FROM Airline_Staff WHERE staff_username = %s and agent_password = MD5(%s)'
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
	agentID = request.form['agentID']
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
		ins = 'INSERT INTO Booking_Agent VALUES(%s, %s, MD5(%s), %s)'
		cursor.execute(ins, (agentID, email, password, airline))
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
		search_flights = 'SELECT * FROM Flight WHERE departure_airport = %s AND arrival_airport = %s AND departure_date = %s AND arrival_date = %s AND trip_type = %s AND departure_date >= DATE(NOW()) AND arrival_date >= DATE(NOW())'
						
		cursor.execute(search_flights, (source, destination, departure, arrival, trip_type))
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
		
		# find airplane id for flight num
		# using airplne id, find seats of that plane
		# divide tickets/seats * 100
		# if > 70, sold_price = base price * 1.2, else base_price = base_price

		for ticket_ID in ticket_IDs:

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
			find_seats = 'SELECT COUNT(ticket_ID) AS tickets_purchased FROM Customer_Purchases WHERE flight_num = %s'
			cursor.execute(find_seats, (flight_purchase))
			tickets_purchased = cursor.fetchone()
			tickets_purchased = int(tickets_purchased['tickets_purchased'])

			# Determine the capacity of the flight by dividing the number of tickets purchased by the number of seats on the airplane
			capacity = (tickets_purchased / seats) * 100

			# If the capacity of the flight> 70, the sold price is 1.2 * base_price
			if(capacity > 70):
				sold_price = base_price * 1.2
			else:
				sold_price = base_price

			search_tickets = 'SELECT is_Purchased FROM Ticket WHERE ticket_ID = %s'
			cursor.execute(search_tickets, (ticket_ID))
			is_Purchased = cursor.fetchone()
			is_Purchased = is_Purchased['is_Purchased']

			if(is_Purchased == "No"):

				change_ticket_status = 'UPDATE Ticket SET is_purchased = "Yes" WHERE ticket_ID = %s AND is_purchased = "No"'
				cursor.execute(change_ticket_status, (ticket_ID))
				conn.commit()

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
		return render_template('customerHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
							past_flights_info=past_flights_info, future_flights_info=future_flights_info, year_expenses=year_expenses, review="Complete")
	
	
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
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, date_expenses=date_expenses, start_date=start_date, end_date=end_date)


	# Returns default information that is displayed each time the page is loaded or refreshed
	cursor.close()
	return render_template('customerHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
							past_flights_info=past_flights_info, future_flights_info=future_flights_info, year_expenses=year_expenses)

@app.route('/agentHome')
def agentHome():
	username = session['username']
	return render_template('agentHome.html')

@app.route('/staffHome')
def staffHome():
	username = session['username']
	return render_template('staffHome.html')

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
