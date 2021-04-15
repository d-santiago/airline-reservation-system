-- Damaris Santiago and Thomas Molina
-- 2.3 Create Tables

CREATE TABLE Airport(
    airport_name varchar(50),
    city varchar(50) NOT NULL,
    PRIMARY KEY(airport_name)
);

CREATE TABLE Airline(
    airline_name VARCHAR(50),
    PRIMARY KEY(airline_name)
);

CREATE TABLE Airplane(
    airplane_ID VARCHAR(20) NOT NULL,
    airline_name VARCHAR(50) NOT NULL,
    seats INT(100) NOT NULL,
    PRIMARY KEY(airplane_ID),
    FOREIGN KEY(airline_name) REFERENCES Airline(airline_name)
);

CREATE TABLE Airline_Staff(
    airline_name VARCHAR(50) NOT NULL,
    staff_username  VARCHAR(50),
    staff_password VARCHAR(50) NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    staff_DOB NUMERIC(8) NOT NULL,
    PRIMARY KEY(staff_username),
    FOREIGN KEY(airline_name) REFERENCES Airline(airline_name)
);

CREATE TABLE Airline_Staff_Phones(
    staff_username VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    FOREIGN KEY(staff_username) REFERENCES Airline_Staff(staff_username)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE Booking_Agent(
    airline_name VARCHAR(50) NOT NULL,
    agent_email VARCHAR(50),
    agent_password VARCHAR(50),
    agent_ID VARCHAR(50),
    PRIMARY KEY(agent_email, agent_password, agent_ID),
    FOREIGN KEY(airline_name) REFERENCES Airline(airline_name)
);

CREATE TABLE Customer(
    cus_email VARCHAR(50),
    cus_password VARCHAR(20) NOT NULL,
    cus_name VARCHAR(50) NOT NULL,
    cus_address VARCHAR(50) NOT NULL,
    cus_building_num VARCHAR(10) NOT NULL,
    cus_street VARCHAR(50) NOT NULL,
    cus_city VARCHAR(50) NOT NULL,
    cus_state VARCHAR(50) NOT NULL,
    cus_phone_num VARCHAR(20) NOT NULL,
    cus_passport_num VARCHAR(9) NOT NULL,
    cus_passport_exp NUMERIC(8) NOT NULL,
    cus_passport_country VARCHAR(50) NOT NULL,
    cus_dob NUMERIC(8) NOT NULL,
    PRIMARY KEY(cus_email)
);

CREATE TABLE Flight(
    airline_name VARCHAR(50) NOT NULL,
    airplane_ID VARCHAR(20) NOT NULL,
    flight_num VARCHAR(20),
    departure_date DATE,
    departure_time TIME,
    departure_airport VARCHAR(50) NOT NULL,
    arrival_date DATE NOT NULL,
    arrival_time TIME NOT NULL,
    arrival_airport VARCHAR(50) NOT NULL,
    base_price VARCHAR(10) NOT NULL,
    seats_available VARCHAR(3) NOT NULL,
    flight_status VARCHAR(10) NOT NULL,
    PRIMARY KEY(flight_num, departure_date, departure_time),
    FOREIGN KEY(airline_name) REFERENCES Airline(airline_name),
    FOREIGN KEY(airplane_ID) REFERENCES Airplane(airplane_ID)
);

CREATE TABLE Ticket(
    flight_num VARCHAR(20) NOT NULL,
    departure_date DATE NOT NULL,
    departure_time TIME NOT NULL,
    airline_name VARCHAR(50) NOT NULL,
    cus_email VARCHAR(50) NOT NULL,
    agent_ID VARCHAR(50),
    ticket_ID VARCHAR(50),
    sold_price VARCHAR(10) NOT NULL,
    card_type VARCHAR(20) NOT NULL,
    card_num VARCHAR(20) NOT NULL,
    card_name VARCHAR(20) NOT NULL,
    exp_date DATE NOT NULL,
    purchase_date DATE,
    purchase_time TIME NOT NULL,
    is_purchased INT(1) NOT NULL,
    PRIMARY KEY(ticket_ID),
    FOREIGN KEY(flight_num, departure_date, departure_time) REFERENCES Flight(flight_num, departure_date, departure_time),
    FOREIGN KEY(airline_name) REFERENCES Airline(airline_name),
    FOREIGN KEY(cus_email) REFERENCES Customer(cus_email)
);

CREATE TABLE Customer_Purchase(
    cus_email VARCHAR(50) NOT NULL,
    ticket_ID VARCHAR(50) NOT NULL,
    purchase_number INT(10) AUTO_INCREMENT,
    sold_price VARCHAR(10) NOT NULL,
    card_type VARCHAR(20) NOT NULL,
    card_num VARCHAR(20) NOT NULL,
    card_name VARCHAR(20) NOT NULL,
    exp_date DATE,
    purchase_date DATE,
    purchase_time TIME,
    PRIMARY KEY(purchase_number),
    FOREIGN KEY(cus_email) REFERENCES Customer(cus_email),
    FOREIGN KEY(ticket_ID) REFERENCES Ticket(ticket_ID)
);

CREATE TABLE Booking_Agent_Commission(
    ticket_ID VARCHAR(20) NOT NULL,
    agent_email VARCHAR(50)  NOT NULL,
    agent_password VARCHAR(50)  NOT NULL,
    agent_ID VARCHAR(50)  NOT NULL,
    comm_per_ticket VARCHAR(10) NOT NULL,
    tickets_sold VARCHAR(6) NOT NULL,
    comm_total VARCHAR(6) NOT NULL,
    comm_ticket_avg VARCHAR(4) NOT NULL,
    FOREIGN KEY(ticket_ID) REFERENCES Ticket(ticket_ID),
    FOREIGN KEY(agent_email, agent_password, agent_ID) REFERENCES Booking_Agent(agent_email, agent_password, agent_ID)
);

CREATE TABLE Review(					
    cus_email VARCHAR(50) NOT NULL,
    flight_num VARCHAR(20) NOT NULL,
    review_ID VARCHAR(10) NOT NULL,
    rating NUMERIC(1) NOT NULL,
    comment VARCHAR(140) NOT NULL,
    PRIMARY KEY(review_ID),
    FOREIGN KEY(cus_email) REFERENCES Customer(cus_email),
    FOREIGN KEY(flight_num) REFERENCES Flight(flight_num)
);

CREATE TABLE Customer_Flight_Log(
	cus_email VARCHAR(50) NOT NULL,
	airline_name VARCHAR(50) NOT NULL,
	flight_num VARCHAR(20) NOT NULL,
    ticket_ID VARCHAR(20) NOT NULL,
    review_ID VARCHAR(10) NOT NULL,
    purchase_number INT(10) NOT NULL, 
	cus_flight_log_ID VARCHAR(10),
	previous_flights VARCHAR(5) NOT NULL,
	future_flights VARCHAR(2) NOT NULL,
    ticks_purchased VARCHAR(5) NOT NULL,
	PRIMARY KEY(cus_flight_log_ID),
	FOREIGN KEY(cus_email) REFERENCES Customer(cus_email),
	FOREIGN KEY(airline_name) REFERENCES Airline(airline_name),
	FOREIGN KEY(flight_num) REFERENCES Flight(flight_num),
    FOREIGN KEY(ticket_ID) REFERENCES Ticket(ticket_ID),
    FOREIGN KEY(review_ID) REFERENCES Review(review_ID),
	FOREIGN KEY(purchase_number) REFERENCES Customer_Purchase(purchase_number)
);

CREATE TABLE Airline_Flight_Log(
    airline_name VARCHAR(50) NOT NULL,
    flight_num VARCHAR(20) NOT NULL,
    ticket_ID VARCHAR(20) NOT NULL,
    review_ID VARCHAR(10) NOT NULL,
    cus_flight_log_ID VARCHAR(10) NOT NULL,
    airline_flight_log_ID VARCHAR(10),
    all_ratings VARCHAR(7) NOT NULL,
    all_comments VARCHAR(7) NOT NULL,
    avg_rating NUMERIC(1) NOT NULL,
    ticks_sold VARCHAR(10) NOT NULL,
    PRIMARY KEY(airline_flight_log_ID),
    FOREIGN KEY(airline_name) REFERENCES Airline(airline_name),
    FOREIGN KEY(flight_num) REFERENCES Flight(flight_num),
    FOREIGN KEY(ticket_ID) REFERENCES Ticket(ticket_ID),
    FOREIGN KEY(review_ID) REFERENCES Review(review_ID),
    FOREIGN KEY(cus_flight_log_ID) REFERENCES Customer_Flight_Log(cus_flight_log_ID)
);

CREATE TABLE Airline_All_Flights_Log(
	cus_flight_log_ID VARCHAR(10) NOT NULL,
    airline_all_flights_log_ID VARCHAR(10),
    most_freq_cus_this_year VARCHAR(50) NOT NULL,
    ticks_sold_each_month VARCHAR(6) NOT NULL,
    tot_rev VARCHAR(14) NOT NULL,
    PRIMARY KEY(airline_all_flights_log_ID),
    FOREIGN KEY(cus_flight_log_ID) REFERENCES Customer_Flight_Log(cus_flight_log_ID)
);

-- 2.3 Inserts

INSERT INTO Airline
VALUES ("China Eastern")

INSERT INTO Airport
VALUES ("JFK", "NYC"),
("PVG", "Shanghai")

INSERT INTO Customer
VALUES ("des538@nyu.edu", "538des", "Damaris Santiago", "6", "MetroTech", "Brooklyn", "NY", 19875260298, "PN5030483", 05042028, "United States of America", 03182000), 
("tm3083@nyu.edu", "3083tm", "Thomas Molina", "6", "MetroTech", "Brooklyn", "NY", 13500986696, "PN2701932", 04292027, "United States of America", 07142000)
INSERT INTO Booking_Agent
VALUES ("China Eastern", "joebiden@chinaeastern.com", "pswd", "BAID0430163990")

INSERT INTO Airplane
VALUES ("APID1214444858", "China Eastern", 100),
("APID3162048293", "China Eastern", 100)

INSERT INTO Airline_Staff
VALUES ("China Eastern", "KHarris2020", "qwerty23", "Kamala", "Harris", 10201964)

INSERT INTO Flight
VALUES ("China Eastern", "APID1214444858", "FNUM7544192432", 20210330, 120000,  "JFK", 20210331,150000, "750.00", 100, "PVG", "On Time"),
("China Eastern", "APID3162048293", "FNUM5438131658", 20210331, 150000,  "JFK",  20210401, 180000, "750.00", 100, "PVG", "On Time"),
("China Eastern", "APID1214444858", "FNUM4958931105", 20210401, 180000,  "JFK", 20210402, 210000, "750.00", 100, "PVG", "Delayed")

INSERT INTO TICKET
VALUES ("FNUM7544192432", 20210330, 120000, "China Eastern", "des538@nyu.edu", NULL, "1", "750.00", "VISA", "503596122675568", "Damaris Santiago", 20241201, 20210318, 120000, 1),
("FNUM7544192432", 20210330, 120000, "China Eastern", "tm3083@nyu.edu", "BAID0430163990", "2", "750.00", "VISA", "187727290949075", "Thomas Molina", 20221201, 20210318, 123000, 1)

-- 2.4 Queries

SELECT flight_num
FROM Flight
WHERE departure_date > (SELECT CURRENT_DATE)

SELECT flight_num
FROM Flight
WHERE flight_status = "Delayed"

SELECT Customer.cus_name
FROM Customer, Ticket
WHERE Customer.cus_email = Ticket.cus_email

SELECT Customer.cus_name
FROM Customer, Ticket
WHERE Ticket.agent_ID IS NOT NULL AND Customer.cus_email = Ticket.cus_email

SELECT airplane_ID
FROM Airplane
WHERE airline_name = "China Eastern"
