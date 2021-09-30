INSERT INTO Airline
VALUES
("United");

INSERT INTO Airline_Staff
VALUES
("Roe", "Jones", "admin", MD5("abcd"), 19641020, "111-2222-3333", "United");

INSERT INTO Airplane (airline_name, seats)
VALUES
("United", "4"),
("United", "4"),
("United", "50");

INSERT INTO Airport
VALUES
("JFK", "NYC"),
("BOS", "Boston"),
("PVG", "Shanghai"),
("BEI", "Beijing"),
("SHEN", "Shenzhen"),
("SFO", "San Francisco"),
("LAX", "Los Angles"),
("HKA", "Hong Kong");

INSERT INTO Booking_Agent (agent_email, agent_password, airline_name)
VALUES
("ctrip@agent.com", MD5("abcd1234"), "United"),
("expedia@agent.com", MD5("abcd1234"), "United");

INSERT INTO Customer
VALUES
("Test Customer 1", "testcustomer@nyu.edu", MD5("1234"), "1555", "Jay St", "Brooklyn", "New York", "123-4321-4321", 19991219, "54321", 20251224, "USA"),
("User 1", "user1@nyu.edu", MD5("1234"), "5405", "Jay St", "Brooklyn", "New York", "123-4322-4322", 19991119, "54322", 20251225, "USA"),
("User 2", "user2@nyu.edu", MD5("1234"), "1702", "Jay St", "Brooklyn", "New York", "123-4323-4323", 19991019, "54323", 20251024, "USA"),
("User 3", "user3@nyu.edu", MD5("1234"), "1890", "Jay St", "Brooklyn", "New York", "123-4324-4324", 19990919, "54324", 20250924, "USA"); 

INSERT INTO Flight (flight_num, airline_name, airplane_ID, departure_airport, departure_date, departure_time, arrival_airport, arrival_date, arrival_time, base_price, flight_status, trip_type)
VALUES
(102, "United", 3, "SFO", 20210412, 132525, "LAX", 20210412, 165025, "300.00", "On Time", "One Way"),
(104, "United", 3, "PVG", 20210514, 132525, "BEI", 20210514, 165025, "300.00", "On Time", "One Way"),
(106, "United", 3, "SFO", 20210312, 132525, "LAX", 20210312, 165025, "350.00", "Delayed", "One Way"),
(206, "United", 2, "SFO", 20210612, 132525, "LAX", 20210612, 165025, "400.00", "On Time", "One Way"),
(207, "United", 2, "LAX", 20210712, 132525, "SFO", 20210712, 165025, "300.00", "On Time", "One Way"),
(134, "United", 3, "JFK", 20210212, 132525, "BOS", 20210212, 165025, "300.00", "Delayed", "One Way"),
(296, "United", 1, "PVG", 20210601, 132525, "SFO", 20210601, 165025, "3000.00", "On Time", "One Way"),
(715, "United", 1, "PVG", 20210428, 102525, "BEI", 20210428, 135025, "500.00", "Delayed", "One Way"),
(839, "United", 3, "SHEN", 20200712, 132525, "BEI", 20200712, 165025, "800.00", "On Time", "One Way");

INSERT INTO Ticket (ticket_ID, flight_num, departure_date, departure_time, airline_name, is_purchased)
VALUES
(1, 102, 20210412, 132525, "United", "No"),
(2, 102, 20210412, 132525, "United", "No"),
(3, 102, 20210412, 132525, "United", "No"),
(4, 104, 20210514, 132525, "United", "No"),
(5, 104, 20210514, 132525, "United", "No"),
(6, 106, 20210312, 132525, "United", "No"),
(7, 106, 20210312, 132525, "United", "No"),
(8, 839, 20200712, 132525, "United", "No"),
(9, 102, 20210412, 132525, "United", "No"),
(11, 134, 20210212, 132525, "United", "No"),
(12, 715, 20210428, 102525, "United", "No"),
(14, 206, 20210612, 132525, "United", "No"),
(15, 206, 20210612, 132525, "United", "No"),
(16, 206, 20210612, 132525, "United", "No"),
(17, 207, 20210712, 132525, "United", "No"),
(18, 207, 20210712, 132525, "United", "No"),
(19, 296, 20210601, 132525, "United", "No"),
(20, 296, 20210601, 132525, "United", "No");

INSERT INTO CUSTOMER_PURCHASES (cus_email, ticket_ID, flight_num, sold_price, card_type, card_num, card_name, card_exp_date, purchase_date, purchase_time, agent_ID)
VALUES
("testcustomer@nyu.edu", 1, 102, "300.00", "credit", "1111-2222-3333-4444", "Test Customer 1", 20230301, 20210312, 115555, 1),
("user1@nyu.edu", 2, 102, "300.00", "credit", "1111-2222-3333-5555", "User 1", 20230301, 20210311, 115555, null),
("user2@nyu.edu", 3, 102, "300.00", "credit", "1111-2222-3333-5555", "User 2", 20230301, 20210411, 115555, null),
("user1@nyu.edu", 4, 104, "300.00", "credit", "1111-2222-3333-5555", "User 1", 20230301, 20210321, 115555, null),
("testcustomer@nyu.edu", 5, 104, "300.00", "credit", "1111-2222-3333-4444", "Test Customer 1", 20230301, 20210428, 115555, 1),
("testcustomer@nyu.edu", 6, 106, "350.00", "credit", "1111-2222-3333-4444", "Test Customer 1", 20230301, 20210305, 115555, 1),
("user3@nyu.edu", 7, 106, "350.00", "credit", "1111-2222-3333-5555", "User 3", 20230301, 20210203, 115555, null),
("user3@nyu.edu", 8, 839, "300.00", "credit", "1111-2222-3333-5555", " User 3", 20230301, 20200703, 115555, null),
("user3@nyu.edu", 9, 102, "360.00", "credit", "1111-2222-3333-5555", "User 3", 20230301, 20210203, 115555, null),
("user3@nyu.edu", 11, 134, "300.00", "credit", "1111-2222-3333-5555", "User 3", 20230301, 20200723, 115555, 2),
("testcustomer@nyu.edu", 12, 715, "500.00", "credit", "1111-2222-3333-4444", "Test Customer 1", 20230301, 20210305, 115555, 1),
("user3@nyu.edu", 14, 206, "400.00", "credit", "1111-2222-3333-5555,", "User 3", 20230301, 20210505, 115555, 1),
("user1@nyu.edu", 15, 206, "400.00", "credit", "1111-2222-3333-5555", "User 1", 20230301, 20210606, 115555, null),
("user2@nyu.edu", 16, 206, "400.00", "credit", "1111-2222-3333-5555", "User 2", 20230301, 20210419, 115555, null),
("user1@nyu.edu", 17, 207, "300.00", "credit", "1111-2222-3333-5555", "User 1", 20230301, 20210311, 115555, 1),
("testcustomer@nyu.edu", 18, 207, "300.00", "credit", "1111-2222-3333-4444", "Test Customer 1", 20230301, 20210425, 115555, 1),
("user1@nyu.edu", 19, 296, "3000.00", "credit", "1111-2222-3333-5555", "User 1", 20230301, 20210504, 115555, 2),
("testcustomer@nyu.edu", 20, 296, "3000.00", "credit", "1111-2222-3333-4444", "Test Customer 1", 20230301, 20210212, 115555, null);

INSERT INTO Review (cus_email, flight_num, rating, comment)
VALUES
("testcustomer@nyu.edu", 102, "4", "Very Comfortable"),
("user1@nyu.edu", 102, "5", "Relaxing, check-in and onboarding very professional"),
("user2@nyu.edu", 102, "3", "Satisfied and will use the same flight again"),
("testcustomer@nyu.edu", 104, "1", "Customer Care services are not good"),
("user1@nyu.edu", 104, "5", "Comfortable journey and Professional");





