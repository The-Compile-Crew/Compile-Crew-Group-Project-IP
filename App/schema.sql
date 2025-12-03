-- User table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT,
    type TEXT NOT NULL
);

-- Applicants table
CREATE TABLE IF NOT EXISTS applicants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT,
    student_id TEXT,
    details TEXT,
    position_id INTEGER,
    status TEXT,
    applied_date TEXT
);
