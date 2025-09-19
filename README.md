# MOCK
🎯 Marketing Campaign Tracker Application
This is a marketing campaign manager application designed to help marketing professionals plan, execute, and track campaigns. It features campaign management, customer segmentation, performance tracking, and a real-time dashboard.

🚀 Features
Campaign Management: Create, update, and delete marketing campaigns with details such as budget, dates, and descriptions.

Customer Segmentation: Manage customer data and create dynamic segments based on attributes.

Performance Tracking: A dashboard to visualize key metrics like emails sent, opened, and clicks.

Business Insights: Real-time analytics on campaign performance using aggregate functions like COUNT, SUM, AVG, MIN, and MAX.

🛠️ Technology Stack
Frontend: Python with the Streamlit library.

Backend: Python for business logic and data handling.

Database: PostgreSQL for data storage, connected via Psycopg2.

📁 Repository Structure
marketing_campaign_[Rollno]/
├── frontend_mar.py          # Streamlit user interface
├── backend_mar.py           # Database connection and business logic
└── database_schema.sql      # PostgreSQL schema definition
📋 Getting Started
Prerequisites
Python 3.8+

PostgreSQL 12+

pip package manager

Installation
Clone the repository:

Bash

git clone https://github.com/your-username/marketing_campaign_[Rollno].git
cd marketing_campaign_[Rollno]
Install Python dependencies:

Bash

pip install streamlit psycopg2-binary
Set up the PostgreSQL database:

Create a new database named marketing_db.

Execute the SQL commands from database_schema.sql to create the necessary tables.

Configure the database connection:

Open backend_mar.py and update the database credentials with your own:

Python

DB_NAME = "marketing_db"
DB_USER = "postgres"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"
Running the Application
From the project root directory, run the Streamlit application:

Bash

streamlit run frontend_mar.py
The application will open in your default web browser.

📈 Database Schema
The database is designed with an Entity-Relationship Model to handle campaigns, customers, and performance metrics. It follows principles of normalization to ensure data integrity and avoid redundancy.

Entity	Description	Relationships
campaigns	Manages campaign details.	One-to-many with campaign_channels and campaign_metrics.
customers	Stores customer data.	Many-to-many with segments via a link table.
segments	Defines dynamic customer groups.	Many-to-many with customers via a link table.
campaign_channels	Details of a campaign's channels.	One-to-many from campaigns, one-to-many with campaign_metrics.
campaign_metrics	Performance data for each channel.	One-to-one with campaign_channels.

Export to Sheets
🔒 ACID Compliance
The application's database operations are designed to be ACID compliant, ensuring data reliability and integrity.

Atomicity: Transactions are treated as a single unit. If any part of a transaction fails, the entire transaction is rolled back, leaving the database unchanged. This is handled by psycopg2's transaction management and explicit commit() and rollback() calls.

Consistency: The database always moves from one valid state to another. This is enforced by foreign key constraints and unique constraints in the schema.

Isolation: Concurrent transactions are isolated from each other. Changes made by one user are not visible to others until the transaction is fully committed.

Durability: Once a transaction is committed, the changes are permanent and will survive a system crash.
