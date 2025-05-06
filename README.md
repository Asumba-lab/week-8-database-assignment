##Library Management System & Task Manager API
 ##Week 8 Assignment: Database Systems + CRUD API Implementation

This repository contains two complete projects:

1.A Library Management System database implemented in MySQL

2.A Task Manager CRUD API built with Python FastAPI and MySQL

 ##Part 1: Library Management Database

 ##Database Schema Overview

A comprehensive library management system with:

Members tracking

Books inventory

Loans management

Fines system

Authors information

 ## Key Features
Proper relational design with 6 normalized tables

Constraints (PK, FK, NOT NULL, UNIQUE, CHECK)

All three relationship types (1-1, 1-M, M-M)

Sample data for demonstration

 ## Setup Instructions

1.Run the SQL script in MySQL:

2.Or import directly in MySQL Workbench

## Database Schema Diagrams (in the Doc)

### Library Management System

### Task Manager System



  ##Part 2: Task Manager API

 ###Features

User authentication system

Full CRUD operations for tasks

Task status and priority management

MySQL database backend

Secure password hashing

  ###Technologies Used
Python 3.9+

FastAPI

MySQL

Passlib (for password hashing)

MySQL Connector/Python

  ###Installation

1.Clone the repository:

git clone https://github.com/yourusername/week8-assignment.git
cd week8-assignment

2.Set up the database:

3.Install dependencies:

4.Run the API

 ## API Documentation

Access the interactive docs at http://localhost:8000/docs after running the server

 ### API Endpoints

Method	                 Endpoint	                                Description
POST	     /users/             	                                 Create new user
POST       	/users/{user_id}/tasks/                         	     Create task for user
GET	         /users/{user_id}/tasks/ 	                             Get all tasks for user
PUT     	/tasks/{task_id}	                                     Update specific task
DELETE  	/tasks/{task_id}    	                                 Delete specific task

 ## Project Structure
week 8 database assignment/
├── main.py             # Your FastAPI application
|-management system.sql
├── requirements.txt    # Dependencies file
├── task_manager.sql    # Database schemats (PK, FK, NOT NULL, UNIQUE)
|-README.md

## Assignment Requirements Checklist

###For Question 1 (Database):

Real-world use case (Library Management)

Well-structured relational database

Proper constraints (PK, FK, NOT NULL, UNIQUE)

All relationship types implemented

Single SQL file with CREATE TABLE statements

Sample data included

###For Question 2 (CRUD API):

Use case (Task Manager)

Database schema (2-3 tables)

Complete CRUD operations

FastAPI implementation

MySQL connection

Proper project organization
