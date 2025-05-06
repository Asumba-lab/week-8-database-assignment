-- Library Management System Database
-- Created by [Your Name] for Week 8 Assignment

-- Database creation
DROP DATABASE IF EXISTS library_management;
CREATE DATABASE library_management;
USE library_management;

-- Members table
CREATE TABLE members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    join_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    membership_status ENUM('active', 'expired', 'suspended') DEFAULT 'active',
    CHECK (email LIKE '%@%.%')
);


-- Books table
CREATE TABLE books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    publisher VARCHAR(100),
    publication_year INT,
    genre VARCHAR(50),
    available_copies INT NOT NULL DEFAULT 1,
    total_copies INT NOT NULL DEFAULT 1,
    CHECK (available_copies <= total_copies),
    CHECK (publication_year BETWEEN 1500 AND 2100) -- Static year range
);

-- Loans table (1-M relationship between members and loans, and books and loans)
CREATE TABLE loans (
    loan_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    book_id INT NOT NULL,
    loan_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    due_date DATE NOT NULL DEFAULT (DATE_ADD(CURRENT_DATE, INTERVAL 14 DAY)),
    return_date DATE,
    status ENUM('active', 'returned', 'overdue') DEFAULT 'active',
    FOREIGN KEY (member_id) REFERENCES members(member_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    CHECK (due_date > loan_date),
    CHECK (return_date IS NULL OR return_date >= loan_date)
);

-- Fines table (1-1 relationship with loans)
CREATE TABLE fines (
    fine_id INT AUTO_INCREMENT PRIMARY KEY,
    loan_id INT UNIQUE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    issue_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    payment_date DATE,
    status ENUM('unpaid', 'paid') DEFAULT 'unpaid',
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),
    CHECK (amount > 0),
    CHECK (payment_date IS NULL OR payment_date >= issue_date)
);

-- Authors table (M-M relationship with books through book_authors)
CREATE TABLE authors (
    author_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_year INT,
    death_year INT,
    biography TEXT
);

-- Junction table for M-M relationship between books and authors
CREATE TABLE book_authors (
    book_id INT NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY (book_id, author_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (author_id) REFERENCES authors(author_id)
);

-- Sample data insertion
-- Insert into members using alias 'm' instead of deprecated VALUES()
INSERT INTO members (first_name, last_name, email, phone, join_date, membership_status)
VALUES
  ('John', 'Smith', 'john.smith@email.com', '555-0101', '2022-01-15', 'active'),
  ('Emily', 'Johnson', 'emily.j@email.com', '555-0102', '2022-03-22', 'active'),
  ('Michael', 'Williams', 'michael.w@email.com', NULL, '2022-05-10', 'suspended') AS m
ON DUPLICATE KEY UPDATE
  phone = m.phone,
  join_date = m.join_date,
  membership_status = m.membership_status;

-- Insert into books with alias 'b'
INSERT INTO books (isbn, title, author, publisher, publication_year, genre, available_copies, total_copies)
VALUES
  ('978-0061120084', 'To Kill a Mockingbird', 'Harper Lee', 'HarperCollins', 1960, 'Fiction', 3, 5),
  ('978-0451524935', '1984', 'George Orwell', 'Signet Classics', 1949, 'Dystopian', 1, 2),
  ('978-0743273565', 'The Great Gatsby', 'F. Scott Fitzgerald', 'Scribner', 1925, 'Classic', 0, 1) AS b
ON DUPLICATE KEY UPDATE
  title = b.title,
  author = b.author,
  publisher = b.publisher,
  publication_year = b.publication_year,
  genre = b.genre,
  available_copies = b.available_copies,
  total_copies = b.total_copies;

-- Insert into authors with alias 'a'
INSERT INTO authors (first_name, last_name, birth_year, death_year)
VALUES
  ('Harper', 'Lee', 1926, 2016),
  ('George', 'Orwell', 1903, 1950),
  ('F. Scott', 'Fitzgerald', 1896, 1940) AS a
ON DUPLICATE KEY UPDATE
  birth_year = a.birth_year,
  death_year = a.death_year;

-- Insert into book_authors ONLY if not already present
INSERT IGNORE INTO book_authors (book_id, author_id) VALUES
  (1, 1), (2, 2), (3, 3);
