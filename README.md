vrn-assignment: Event Management System

Project Overview

This project is a web-based event management system designed to facilitate event creation, registration, and reporting for users, managers, and administrators. It provides a streamlined platform for efficient event organization and management.

Roles and Responsibilities

Admin:
Holds the highest level of access and control.
Can view comprehensive reports on all users, managers, events, and registrations.
May have additional administrative capabilities depending on the project's specific needs (e.g., managing user roles, system settings).
Manager:
Responsible for creating and managing events.
Can define event details such as name, description, date, time, location, and capacity.
May have the ability to edit or delete events they create.
User:
Can register for events that interest them.
Has the ability to view all available organizations and events listed on the platform.
Project Features

Event Creation: Managers have a dedicated interface to create events, specifying details and potentially setting up event registration forms or collecting additional information from attendees.
Event Registration: Users can register for events they wish to attend. The registration process may involve capturing user information or fulfilling specific requirements set by the manager.
Reporting: The system provides comprehensive reporting functionality for the admin to view user details, manager activities, event information, and registration data. This allows for clear insights into event participation and facilitates informed decision-making.

Technology Stack

Back-End: Django and DRF for RESTful API development
Database: PostgreSQL for efficient data storage
Containerization: Docker for consistent deployment and environment management

Running the vrn-assignment Event Management System with Docker

This guide details how to set up and run your event management system using Docker and Docker Compose.

Prerequisites

Git: Install Git from https://git-scm.com/downloads
Docker: Download and install Docker from https://www.docker.com/get-started (follow instructions for your operating system)
Docker Compose: Install Docker Compose by following the official instructions: https://docs.docker.com/compose/install/
Steps

Clone the Project:

Bash
git clone https://github.com/swapnil-259/vrn-assignment.git
cd vrn-assignment
Use code with caution.

Create Environment Folder and Secret Files:

Create a new folder named env in the project root directory.

Inside the env folder, create two files: pgadmin.env and postgres.env.

In pgadmin.env, add your desired credentials for pgAdmin:

PGADMIN_DEFAULT_EMAIL='your_email@example.com'
PGADMIN_DEFAULT_PASSWORD='your_strong_password'
In postgres.env, define the database credentials:

POSTGRES_DB='vrn_events'  # Replace with your desired database name
POSTGRES_USER='vrn_user'  # Replace with your desired username
POSTGRES_PASSWORD='your_strong_password'  # Replace with your strong password
Important: Replace placeholders with your own email, password, and database name. Ensure the password is strong and unique.

Create a file named secret.py in the project root directory. This file will store sensitive database credentials. Paste the following code into secret.py:
DB_USER='vrn_events'  # Replace with your desired database name
DB_USER='vrn_user'  # Replace with your desired username
DB_PASSWORD='your_strong_password'  # Replace with your strong password

These all are same as the postgres.env


Build Docker Images:

Navigate to the project root directory and run the following command in your terminal:

Bash
docker-compose build
Use code with caution.

This command instructs Docker Compose to build the Docker images defined in docker-compose.yml (assuming this file exists in your project root). The docker-compose.yml file specifies the services (containers) required for your application, including the Django server and a Postgres database.

Run the Application:

Start the containers in detached mode (background) using:

Bash
docker-compose up -d
Use code with caution.

This launches the Postgres database and the Django application container. The -d flag instructs Docker Compose to run the services in the background.

Connect to the Django Server:

Option 1: Using Docker Compose:

Docker Compose allows you to access the Django application running inside a container. Run the following command to get an interactive shell within the vrn_django container (replace vrn_django with the actual container name if it's different):

Bash
docker exec -it vrn_django bash
Use code with caution.

Inside this shell, you can run Django commands directly, such as:

Bash
python manage.py runserver 0.0.0.0:8000
Use code with caution.

This starts the Django development server on port 8000 within the container, but it's only accessible from other containers within the Docker network.


Importing Initial Data:

Once you're inside the vrn_django container's shell, you can import the initial data from your db.json file using the Django management command:

Bash
python manage.py loaddata db.json
Use code with caution.

This command reads the data from db.json and populates your database with the corresponding model instances, ensuring your application starts with the necessary data set.


Run the createsuperuser Command:

Inside the container shell, execute the following command to initiate the admin user creation process:

Bash
python manage.py createsuperuser
Use code with caution.

Provide Admin User Details:

You'll be prompted to enter the following information for your admin user:

Username: Choose a username for your admin account. This will be used to log in to the admin panel.
Email address (optional): Provide a valid email address if you want to receive notifications associated with your admin account.
Password: Enter a strong and secure password for your admin user. It's recommended to use a combination of uppercase and lowercase letters, numbers, and symbols for maximum security.
Password (again): Re-type the password to confirm it.
Important: Take note of the username and password you choose, as you'll need them to log in to the Django admin panel.
