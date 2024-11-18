-- Create database
#CREATE DATABASE movie_ticket_booking;

-- Use the database
USE movie_ticket_booking;

-- Create users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100)
);

-- Create movies table
CREATE TABLE movies (
    movie_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    duration INT, -- in minutes
    rating DECIMAL(3, 1)
);

-- Create theaters table
CREATE TABLE theaters (
    theater_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255)
);

-- Create shows table
CREATE TABLE shows (
    show_id INT AUTO_INCREMENT PRIMARY KEY,
    movie_id INT,
    theater_id INT,
    show_time DATETIME,
    seats_available INT,
    FOREIGN KEY (movie_id) REFERENCES movies(movie_id),
    FOREIGN KEY (theater_id) REFERENCES theaters(theater_id)
);

-- Create bookings table
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    show_id INT,
    number_of_tickets INT,
    booking_time DATETIME,
    payment_status ENUM('Pending', 'Paid'),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (show_id) REFERENCES shows(show_id)
);

-- Insert some sample movies
INSERT INTO movies (title, genre, duration, rating) VALUES 
('Avengers: Endgame', 'Action', 181, 8.4),
('The Lion King', 'Animation', 118, 7.0),
('Inception', 'Sci-Fi', 148, 8.8);

-- Insert some sample theaters
INSERT INTO theaters (name, location) VALUES 
('Cinema City', 'Downtown'),
('Movie World', 'Uptown');

-- Insert some sample shows
INSERT INTO shows (movie_id, theater_id, show_time, seats_available) VALUES 
(1, 1, '2024-11-25 18:30:00', 100),
(2, 2, '2024-11-25 20:30:00', 80),
(3, 1, '2024-11-26 15:00:00', 50);

-- Insert sample users
INSERT INTO users (username, password, email) VALUES
('john_doe', 'password123', 'john.doe@example.com'),
('jane_smith', 'mypassword456', 'jane.smith@example.com'),
('alice_johnson', 'alicepass789', 'alice.johnson@example.com');

-- Insert sample bookings
INSERT INTO bookings (user_id, show_id, number_of_tickets, booking_time, payment_status) VALUES
(1, 1, 2, '2024-11-20 14:25:00', 'Paid'),  -- John Doe books 2 tickets for Avengers: Endgame
(2, 2, 1, '2024-11-21 17:10:00', 'Pending'),  -- Jane Smith books 1 ticket for The Lion King
(3, 3, 4, '2024-11-22 12:50:00', 'Paid'),  -- Alice Johnson books 4 tickets for Inception
(1, 3, 3, '2024-11-23 18:00:00', 'Pending');  -- John Doe books 3 tickets for Inception


SELECT * FROM users;
SELECT * FROM movies;
SELECT * FROM theaters;
SELECT * FROM shows;
SELECT * FROM bookings;


