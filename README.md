## Project Title: Flask User Registration and Authentication

### Description

This Flask application provides a simple user registration and authentication system. Users can create accounts, log in, manage their profiles, and update their information securely.

### Features

- User registration with hashed passwords
- User login with session management
- Profile viewing and updating
- Secure password storage using hashing(pbkdf2-sha256)
- Responsive design with HTML/CSS

### Technologies Used

- Flask: Web framework for building the application
- MySQL: Database for storing user data
- Werkzeug: Library for password hashing
- HTML/CSS: Front-end for user interface

### Installation

1.Install the required packages:   

     pip install Flask mysql-connector-python Werkzeug

2.Set up the MySQL database:

  Create a database named register.
      Execute the following SQL command:
       sql

        CREATE TABLE IF NOT EXISTS users (
           pid INT AUTO_INCREMENT PRIMARY KEY,
             name VARCHAR(255) NOT NULL,
              password VARCHAR(255) NOT NULL,
            age INT,
               address VARCHAR(255),
              contact VARCHAR(20),
              mail VARCHAR(255)
           );
4.Run the application:

    python app.py
     
5.Usage:

         Register: Create a new account.
         Login: Access your account with your credentials.
         Profile: View and edit your user profile.
         Logout: End your session.     

