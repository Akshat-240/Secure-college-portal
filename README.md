# Secure College Portal 

A secure web-based authentication system developed as a **1st Semester Cybersecurity Project**. This project demonstrates fundamental security principles including secure password storage, role-based access control, and protection against common web vulnerabilities.

## Project Overview

The **Secure College Portal** provides a platform for Students, Faculty, and Admin to log in securely. It addresses the critical need for protecting user credentials and preventing unauthorized access in educational institutions.

## Key Security Features

This project implements several core cybersecurity concepts:

*   **Secure Password Hashing**:
    *   Passwords are **never** stored in plain text.
    *   Uses **PBKDF2-SHA256** with unique **SALT** for every user.
    *   Protects against Rainbow Table attacks and hash collisions.
    *   Implementation: `werkzeug.security`

*   **Brute Force Protection**:
    *   **Account Lockout Policy**: Use account is automatically locked after **3 failed login attempts**.
    *   Prevents attackers from guessing passwords indefinitely.

*   **Role-Based Access Control (RBAC)**:
    *   Strict segregation of duties between **Student**, **Faculty**, and **Admin**.
    *   Users cannot access dashboards unauthorized for their role (e.g., a Student cannot access the Admin panel).

*   **SQL Injection Prevention**:
    *   All database queries use **Parameterized Queries** (Prepared Statements).
    *   Prevents attackers from manipulating the database via input fields.

## Tech Stack

*   **Language**: Python 3.x
*   **Web Framework**: Flask
*   **Database**: SQLite (Embedded)
*   **Frontend**: HTML5, CSS3 (Modern Glassmorphism UI)
*   **Cryptography**: hashing (werkzeug.security) (PBKDF2)


## 👥 Contributors

*   **Akshat Nigam** - [GitHub](https://github.com/Akshat-240)

---
*This project is for educational purposes to demonstrate secure coding practices.*