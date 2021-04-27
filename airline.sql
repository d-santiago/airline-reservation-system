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
    airplane_ID INT AUTO_INCREMENT,
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
    agent_ID INT AUTO_INCREMENT,
    agent_email VARCHAR(50),
    agent_password VARCHAR(50),
    airline_name VARCHAR(50) NOT NULL,
    PRIMARY KEY(agent_ID, agent_email, agent_password),
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
    flight_num INT AUTO_INCREMENT,
    airline_name VARCHAR(50) NOT NULL,
    airplane_ID INT NOT NULL,
    departure_airport VARCHAR(50) NOT NULL,
    departure_date DATE,
    departure_time TIME,
    arrival_airport VARCHAR(50) NOT NULL,
    arrival_date DATE NOT NULL,
    arrival_time TIME NOT NULL,
    base_price VARCHAR(8) NOT NULL,
    flight_status VARCHAR(50) NOT NULL,
    trip_type VARCHAR(50) NOT NULL,
    PRIMARY KEY(flight_num, departure_date, departure_time),
    FOREIGN KEY(airline_name) REFERENCES Airline(airline_name),
    FOREIGN KEY(airplane_ID) REFERENCES Airplane(airplane_ID)
);

CREATE TABLE Ticket(
    ticket_ID INT AUTO_INCREMENT,
    flight_num INT NOT NULL,
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
    flight_num INT NOT NULL,
    sold_price VARCHAR(8) NOT NULL,
    card_type VARCHAR(50) NOT NULL,
    card_num VARCHAR(50) NOT NULL,
    card_name VARCHAR(50) NOT NULL,
    card_exp_date DATE NOT NULL,
    purchase_date DATE NOT NULL,
    purchase_time TIME NOT NULL,
    agent_ID INT,
    PRIMARY KEY(purchase_ID),
    FOREIGN KEY(cus_email) REFERENCES Customer(cus_email),
    FOREIGN KEY(ticket_ID) REFERENCES Ticket(ticket_ID),
    FOREIGN KEY(flight_num) REFERENCES Flight(flight_num)
);

CREATE TABLE Review(
    review_ID INT AUTO_INCREMENT,					
    cus_email VARCHAR(50) NOT NULL,
    flight_num INT NOT NULL,
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

INSERT INTO Airplane (airline_name, seats)
VALUES ("China Eastern", "100"),
("China Eastern", "100");

INSERT INTO Airline_Staff
VALUES ("Kamala", "Harris", "KHarris2020", MD5("qwerty23"), 19641020, "1(504)000-5322", "China Eastern");

INSERT INTO Booking_Agent (agent_email, agent_password, airline_name)
VALUES ("joebiden@chinaeastern.com", MD5("pswd!"), "China Eastern");

INSERT INTO Customer
VALUES ("Damaris Santiago", "des538@nyu.edu", MD5("des538"), "6", "MetroTech", "Brooklyn", "NY", "1(987)526-0298", 20000318, "PN-1", 20280504, "United States of America"), 
("Thomas Molina", "tm3083@nyu.edu", MD5("tm3083"), "6", "MetroTech", "Brooklyn", "NY", "1(350)098-6696", 20000714, "PN-2", 20270429, "United States of America");

INSERT INTO Flight (airline_name, airplane_ID, departure_airport, departure_date, departure_time, arrival_airport, arrival_date, arrival_time, base_price, flight_status, trip_type)
VALUES ("China Eastern", 1, "JFK", 20210330, 120000, "PVG", 20210331, 150000, "750.00","On Time", "One Way"),
("China Eastern", 2, "JFK", 20210331, 150000, "PVG", 20210401, 180000, "750.00", "Delayed", "One Way"),
("China Eastern", 2, "JFK", 20211201, 150000, "PVG", 20211202, 180000, "750.00", "On Time", "One Way");

INSERT INTO Ticket (flight_num, departure_date, departure_time, airline_name, is_purchased)
VALUES (1, 20210330, 120000, "China Eastern", "Yes"),
(1, 20210330, 120000, "China Eastern", "Yes"),
(1, 20210330, 120000, "China Eastern", "No"),
(1, 20210330, 120000, "China Eastern", "No"),
(1, 20210330, 120000, "China Eastern", "No"),
(1, 20210330, 120000, "China Eastern", "No"),
(3, 20211201, 150000, "China Eastern", "Yes"),
(3, 20211201, 150000, "China Eastern", "No"),
(3, 20211201, 150000, "China Eastern", "No"),
(3, 20211201, 150000, "China Eastern", "No"),
(3, 20211201, 150000, "China Eastern", "No");

INSERT INTO CUSTOMER_PURCHASES (cus_email, ticket_ID, flight_num, sold_price, card_type, card_num, card_name, card_exp_date, purchase_date, purchase_time, agent_ID)
VALUES ("des538@nyu.edu", 1, 1, "750.00", "VISA", "6350-3566-2738-8744", "Damaris Santiago", 20240130, 20210228, 100000, NULL),
("tm3083@nyu.edu", 2, 1, "750.00", "VISA", "8943-8852-8197-4346", "Thomas Molina", 20240430, 20210228, 100100, 1),
("des538@nyu.edu", 7, 3, "750.00", "VISA", "6350-3566-2738-8744", "Damaris Santiago", 20240130, 20210417, 190000, 1);