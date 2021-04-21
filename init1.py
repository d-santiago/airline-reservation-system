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
                       db='AirlineReservationSystem',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
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
	query = 'SELECT * FROM Customer WHERE cus_email = %s and cus_password = %s'
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
	query = 'SELECT * FROM Booking_Agent WHERE agent_email = %s and agent_password = %s'
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
	query = 'SELECT * FROM Airline_Staff WHERE staff_username = %s and agent_password = %s'
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
		ins = 'INSERT INTO Customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
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
		ins = 'INSERT INTO Booking_Agent VALUES(%s, %s, %s, %s)'
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
		ins = 'INSERT INTO Airline_Staff VALUES(%s, %s, %s, %s, %s, %s, %s)'
		cursor.execute(ins, (firstName, lastName, username, password, dob, phone, airline))
		conn.commit()
		cursor.close()
		return render_template('index.html')

@app.route('/customerHome', methods=['GET', 'POST'])
def customerHome():
	username = session['username']

	# When a customer searches for flights
	conduct_flight_search = False;
	if ('package' in request.form and 'source' in request.form and'destination' in request.form and 'departure' in request.form and 'arrival' in request.form):	
		conduct_flight_search = True;
		package = request.form['package']
		source = request.form['source']
		destination = request.form['destination']	
		departure = request.form['departure']
		arrival = request.form['arrival']

	# When books a customer flight that showed up in their search
	conduct_ticket_search = False;
	if ('flight_select' in request.form):
		conduct_ticket_search = True;	
		flight_select = request.form['flight_select']

	# When customer completes the purchase for a flight that showed up in their search
	conduct_ticket_purchase = False;
	if ('flight_purchase' in request.form and 'ticket' in request.form and 'type' in request.form and 'num' in request.form and 'name' in request.form and 'exp' in request.form):	
		conduct_ticket_purchase = True;
		flight_purchase = request.form['flight_purchase']
		ticket_IDs = request.form.getlist('ticket')
		card_type = request.form['type']
		card_num = request.form['num']
		card_name = request.form['name']
		card_exp = request.form['exp']	

	cursor = conn.cursor()
	
	# Finds all flights that a customer has purchased from Customer_Purchases Table
	find_flights = 'SELECT flight_num, ticket_ID FROM Customer_Purchases WHERE cus_email = %s'
	cursor.execute(find_flights, (username))
	all_flights = cursor.fetchall()

	all_flights_info = []
	past_flights_info = []
	future_flights_info = []

	flightsOccured = []

	# Finds additional information about each flight in Flight Table that isn't stored in Cutomer_Purchases Table
	# Uses this information to also determine which flight is from the past or future
	for flight in all_flights:

		if (flight['flight_num'] not in flightsOccured):

			find_all_flights_info = 'SELECT flight_num, airline_name, airplane_ID, departure_airport, departure_date, departure_time, \
									arrival_airport, arrival_date, arrival_time FROM Flight WHERE flight_num = %s'

			cursor.execute(find_all_flights_info, (flight['flight_num']))
			flight_info = cursor.fetchone()
			all_flights_info.append(flight_info)

			flightsOccured.append(flight['flight_num'])

	flightsOccured = []
	for flight in all_flights:

		if (flight['flight_num'] not in flightsOccured):

			find_past_flights_info = 'SELECT flight_num, airline_name, airplane_ID, departure_airport, departure_date, departure_time, \
									arrival_airport, arrival_date, arrival_time FROM Flight WHERE flight_num = %s \
									AND departure_date < DATE(NOW())'

			cursor.execute(find_past_flights_info, (flight['flight_num']))
			flight_info = cursor.fetchone()
			past_flights_info.append(flight_info)

			flightsOccured.append(flight['flight_num'])

	flightsOccured = []
	for flight in all_flights:

		if (flight['flight_num'] not in flightsOccured):

			find_future_flights_info = 'SELECT flight_num, airline_name, airplane_ID, departure_airport, departure_date, departure_time, \
										arrival_airport, arrival_date, arrival_time, flight_status FROM Flight WHERE flight_num = %s \
										AND departure_date > DATE(NOW())'

			cursor.execute(find_future_flights_info, (flight['flight_num']))
			flight_info = cursor.fetchone()
			future_flights_info.append(flight_info)

			flightsOccured.append(flight['flight_num'])

	# Searches for flights
	if (conduct_flight_search == True):
		search_flights = 'SELECT flight_num, airline_name, airplane_ID, departure_airport, departure_date, departure_time, \
						arrival_airport, arrival_date, arrival_time, base_price, flight_status FROM Flight \
						WHERE departure_airport = %s AND arrival_airport = %s AND departure_date = %s AND arrival_date = %s'
						
		cursor.execute(search_flights, (source, destination, departure, arrival))
		query_flights = cursor.fetchall()

		cursor.close()
		return render_template('customerHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, query_flights=query_flights)

	# Reveals a purchase form for the ticket if one is avaiable for the flight selected
	if (conduct_ticket_search == True):
		search_tickets = 'SELECT ticket_ID FROM Ticket WHERE flight_num = %s AND is_purchased = "No"'
		cursor.execute(search_tickets, (flight_select))
		tickets = cursor.fetchall()

		if (not tickets):
			tickets = "No Tickets"

		cursor.close()
		return render_template('customerHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, flight_select=flight_select, tickets=tickets)

	# Completes purchase by updating the Ticket Table and inserting into Customer Purchases
	if (conduct_ticket_purchase == True):
		search_flights = 'SELECT base_price FROM Flight WHERE flight_num = %s'
		cursor.execute(search_flights, (flight_purchase))
		base_price = cursor.fetchone()
		base_price = base_price['base_price']
		# Need to implement: calculating the sold price

		for ticket_ID in ticket_IDs:

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
				cursor.execute(insert_purchase, (username, ticket_ID, flight_purchase, base_price, card_type, card_num, card_name, card_exp))
				conn.commit()

		cursor.close()
		return render_template('customerHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
								past_flights_info=past_flights_info, future_flights_info=future_flights_info, purchase="Complete")

	cursor.close()
	return render_template('customerHome.html', username=username, all_flights=all_flights, all_flights_info=all_flights_info, \
							past_flights_info=past_flights_info, future_flights_info=future_flights_info)

@app.route('/agentHome')
def agentHome():
	username = session['username']
	return render_template('agentHome.html')

@app.route('/staffHome')
def staffHome():
	username = session['username']
	return render_template('staffHome.html')

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 8888
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
