-- Damaris Santiago and Thomas Molina
-- Tables

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
    airplane_ID VARCHAR(50) NOT NULL,
    airline_name VARCHAR(50) NOT NULL,
    seats VARCHAR(3) NOT NULL,
    PRIMARY KEY(airplane_ID),
    FOREIGN KEY(airline_name) REFERENCES Airline(airline_name)
);

CREATE TABLE Airline_Staff(
    staff_first_name VARCHAR(50) NOT NULL,
    staff_last_name VARCHAR(50) NOT NULL,
    staff_username VARCHAR(50),
    staff_password VARCHAR(50) NOT NULL,
    staff_DOB DATE NOT NULL,
    phone VARCHAR(50) NOT NULL,
    airline_name VARCHAR(50) NOT NULL,
    PRIMARY KEY(staff_username),
    FOREIGN KEY(airline_name) REFERENCES Airline(airline_name)
);

CREATE TABLE Booking_Agent(
    agent_ID VARCHAR(50),
    agent_email VARCHAR(50),
    agent_password VARCHAR(50),
    airline_name VARCHAR(50) NOT NULL,
    PRIMARY KEY(agent_email, agent_password, agent_ID),
    FOREIGN KEY(airline_name) REFERENCES Airline(airline_name)
);

CREATE TABLE Customer(
    cus_name VARCHAR(50) NOT NULL,
    cus_email VARCHAR(50),
    cus_password VARCHAR(50) NOT NULL,
    cus_building_num VARCHAR(50) NOT NULL,
    cus_street VARCHAR(50) NOT NULL,
    cus_city VARCHAR(50) NOT NULL,
    cus_state VARCHAR(50) NOT NULL,
    cus_phone_num VARCHAR(50) NOT NULL,
    cus_DOB DATE NOT NULL,
    cus_passport_num VARCHAR(50) NOT NULL,
    cus_passport_exp DATE NOT NULL,
    cus_passport_country VARCHAR(50) NOT NULL,
    PRIMARY KEY(cus_email)
);

CREATE TABLE Flight(
    flight_num VARCHAR(50),
    airline_name VARCHAR(50) NOT NULL,
    airplane_ID VARCHAR(50) NOT NULL,
    departure_airport VARCHAR(50) NOT NULL,
    departure_date DATE,
    departure_time TIME,
    arrival_airport VARCHAR(50) NOT NULL,
    arrival_date DATE NOT NULL,
    arrival_time TIME NOT NULL,
    base_price VARCHAR(8) NOT NULL,
    seats_available VARCHAR(3) NOT NULL,
    flight_status VARCHAR(50) NOT NULL,
    trip_type VARCHAR(50) NOT NULL,
    PRIMARY KEY(flight_num, departure_date, departure_time),
    FOREIGN KEY(airline_name) REFERENCES Airline(airline_name),
    FOREIGN KEY(airplane_ID) REFERENCES Airplane(airplane_ID)
);

CREATE TABLE Ticket(
    ticket_ID INT AUTO_INCREMENT,
    flight_num VARCHAR(50) NOT NULL,
    departure_date DATE NOT NULL,
    departure_time TIME NOT NULL,
    airline_name VARCHAR(50) NOT NULL,
    is_purchased VARCHAR(3) NOT NULL,
    PRIMARY KEY(ticket_ID),
    FOREIGN KEY(flight_num, departure_date, departure_time) REFERENCES Flight(flight_num, departure_date, departure_time),
    FOREIGN KEY(airline_name) REFERENCES Airline(airline_name)
);

CREATE TABLE Customer_Purchases(
    purchase_ID INT AUTO_INCREMENT,
    cus_email VARCHAR(50) NOT NULL,
    ticket_ID INT NOT NULL,
    flight_num VARCHAR(50) NOT NULL,
    sold_price VARCHAR(8) NOT NULL,
    card_type VARCHAR(50) NOT NULL,
    card_num VARCHAR(50) NOT NULL,
    card_name VARCHAR(50) NOT NULL,
    card_exp_date DATE NOT NULL,
    purchase_date DATE NOT NULL,
    purchase_time TIME NOT NULL,
    agent_ID VARCHAR(50),
    PRIMARY KEY(purchase_ID),
    FOREIGN KEY(cus_email) REFERENCES Customer(cus_email),
    FOREIGN KEY(ticket_ID) REFERENCES Ticket(ticket_ID),
    FOREIGN KEY(flight_num) REFERENCES Flight(flight_num)
);

CREATE TABLE Review(
    review_ID INT AUTO_INCREMENT,					
    cus_email VARCHAR(50) NOT NULL,
    flight_num VARCHAR(50) NOT NULL,
    rating VARCHAR(1) NOT NULL,
    comment VARCHAR(1000) NOT NULL,
    PRIMARY KEY(review_ID),
    FOREIGN KEY(cus_email) REFERENCES Customer(cus_email),
    FOREIGN KEY(flight_num) REFERENCES Flight(flight_num)
);

-- Inserts

INSERT INTO Airport
VALUES ("JFK", "NYC"),
("PVG", "Shanghai");

INSERT INTO Airline
VALUES ("China Eastern");

INSERT INTO Airplane
VALUES ("APID-1", "China Eastern", "100"),
("APID-2", "China Eastern", "100");

INSERT INTO Airline_Staff
VALUES ("Kamala", "Harris", "KHarris2020", MD5("qwerty23"), 19641020, "1(504)000-5322", "China Eastern");

INSERT INTO Booking_Agent
VALUES ("BA-1", "joebiden@chinaeastern.com", MD5("pswd!"), "China Eastern");

INSERT INTO Customer
VALUES ("Damaris Santiago", "des538@nyu.edu", MD5("des538"), "6", "MetroTech", "Brooklyn", "NY", "1(987)526-0298", 20000318, "PN-1", 20280504, "United States of America"), 
("Thomas Molina", "tm3083@nyu.edu", MD5("tm3083"), "6", "MetroTech", "Brooklyn", "NY", "1(350)098-6696", 20000714, "PN-2", 20270429, "United States of America");

INSERT INTO Flight
VALUES ("FN-1", "China Eastern", "APID-1", "JFK", 20210330, 120000, "PVG", 20210331, 150000, "750.00", "100", "On Time", "One Way"),
("FN-2", "China Eastern", "APID-2", "JFK", 20210331, 150000, "PVG", 20210401, 180000, "750.00", "100", "Delayed", "One Way"),
("FN-3", "China Eastern", "APID-2", "JFK", 20211201, 150000, "PVG", 20211202, 180000, "750.00", "100", "On Time", "One Way");

INSERT INTO TICKET (flight_num, departure_date, departure_time, airline_name, is_purchased)
VALUES ("FN-1", 20210330, 120000, "China Eastern", "Yes"),
("FN-1", 20210330, 120000, "China Eastern", "Yes"),
("FN-1", 20210330, 120000, "China Eastern", "No"),
("FN-1", 20210330, 120000, "China Eastern", "No"),
("FN-1", 20210330, 120000, "China Eastern", "No"),
("FN-1", 20210330, 120000, "China Eastern", "No"),
("FN-3", 20211201, 150000, "China Eastern", "Yes"),
("FN-3", 20211201, 150000, "China Eastern", "No"),
("FN-3", 20211201, 150000, "China Eastern", "No"),
("FN-3", 20211201, 150000, "China Eastern", "No"),
("FN-3", 20211201, 150000, "China Eastern", "No");

INSERT INTO CUSTOMER_PURCHASES (cus_email, ticket_ID, flight_num, sold_price, card_type, card_num, card_name, card_exp_date, purchase_date, purchase_time, agent_ID)
VALUES ("des538@nyu.edu", 1, "FN-1", "750.00", "VISA", "6350-3566-2738-8744", "Damaris Santiago", 20240130, 20210228, 100000, NULL),
("tm3083@nyu.edu", 2, "FN-1", "750.00", "VISA", "8943-8852-8197-4346", "Thomas Molina", 20240430, 20210228, 100100, "BAID-1"),
("des538@nyu.edu", 7, "FN-3", "750.00", "VISA", "6350-3566-2738-8744", "Damaris Santiago", 20240130, 20210417, 190000, NULL);

-- Queries

-- SELECT flight_num
-- FROM Flight
-- WHERE departure_date > (SELECT CURRENT_DATE)

-- SELECT flight_num
-- FROM Flight
-- WHERE flight_status = "Delayed"

-- SELECT Customer.cus_name
-- FROM Customer, Ticket
-- WHERE Customer.cus_email = Ticket.cus_email

-- SELECT Customer.cus_name
-- FROM Customer, Ticket
-- WHERE Ticket.agent_ID IS NOT NULL AND Customer.cus_email = Ticket.cus_email

-- SELECT airplane_ID
-- FROM Airplane
-- WHERE airline_name = "China Eastern"

-- More Tables (Unnecessary)

-- CREATE TABLE Booking_Agent_Commission(
--     ticket_ID INT AUTO_INCREMENT NOT NULL,
--     agent_email VARCHAR(50) NOT NULL,
--     agent_password VARCHAR(50) NOT NULL,
--     agent_ID VARCHAR(50) NOT NULL,
--     tickets_sold VARCHAR(10) NOT NULL,
--     comm_total VARCHAR(10) NOT NULL,
--     comm_per_ticket VARCHAR(10) NOT NULL,
--     comm_ticket_avg VARCHAR(10) NOT NULL,
--     FOREIGN KEY(ticket_ID) REFERENCES Ticket(ticket_ID),
--     FOREIGN KEY(agent_email, agent_password, agent_ID) REFERENCES Booking_Agent(agent_email, agent_password, agent_ID)
-- );

-- CREATE TABLE Customer_Flight_Log(
--     cus_flight_log_ID INT AUTO_INCREMENT,
--     cus_email VARCHAR(50) NOT NULL,
--     airline_name VARCHAR(50) NOT NULL,
--     flight_num VARCHAR(50) NOT NULL,
--     ticket_ID VARCHAR(50) NOT NULL,
--     review_ID INT NOT NULL,
--     purchase_ID INT NOT NULL,
--     previous_flights VARCHAR(5) NOT NULL,
--     future_flights VARCHAR(2) NOT NULL,
--     ticks_purchased VARCHAR(5) NOT NULL,
--     PRIMARY KEY(cus_flight_log_ID),
--     FOREIGN KEY(cus_email) REFERENCES Customer(cus_email),
--     FOREIGN KEY(airline_name) REFERENCES Airline(airline_name),
--     FOREIGN KEY(flight_num) REFERENCES Flight(flight_num),
--     FOREIGN KEY(ticket_ID) REFERENCES Ticket(ticket_ID),
--     FOREIGN KEY(review_ID) REFERENCES Review(review_ID),
--     FOREIGN KEY(purchase_ID) REFERENCES Customer_Purchases(purchase_ID)
-- );

-- CREATE TABLE Airline_Flight_Log(
--     airline_name VARCHAR(50) NOT NULL,
--     flight_num VARCHAR(50) NOT NULL,
--     ticket_ID VARCHAR(20) NOT NULL,
--     review_ID VARCHAR(10) NOT NULL,
--     cus_flight_log_ID INT NOT NULL,
--     airline_flight_log_ID VARCHAR(10),
--     all_ratings VARCHAR(7) NOT NULL,
--     all_comments VARCHAR(7) NOT NULL,
--     avg_rating NUMERIC(1) NOT NULL,
--     ticks_sold VARCHAR(10) NOT NULL,
--     PRIMARY KEY(airline_flight_log_ID),
--     FOREIGN KEY(airline_name) REFERENCES Airline(airline_name),
--     FOREIGN KEY(flight_num) REFERENCES Flight(flight_num),
--     FOREIGN KEY(ticket_ID) REFERENCES Ticket(ticket_ID),
--     FOREIGN KEY(review_ID) REFERENCES Review(review_ID),
--     FOREIGN KEY(cus_flight_log_ID) REFERENCES Customer_Flight_Log(cus_flight_log_ID)
-- );

-- CREATE TABLE Airline_All_Flights_Log(
--     cus_flight_log_ID INT NOT NULL,
--     airline_all_flights_log_ID VARCHAR(10),
--     most_freq_cus_this_year VARCHAR(50) NOT NULL,
--     ticks_sold_each_month VARCHAR(6) NOT NULL,
--     tot_rev VARCHAR(14) NOT NULL,
--     PRIMARY KEY(airline_all_flights_log_ID),
--     FOREIGN KEY(cus_flight_log_ID) REFERENCES Customer_Flight_Log(cus_flight_log_ID)
-- );