# Project Statement

## Problem statement

Student information such as roll number, course, marks, and attendance can be difficult to maintain consistently in separate paper or spreadsheet records. This project provides a simple web application to keep these details together and make common record operations easier.

## Scope

The application stores student records in a local SQLite database. Users can add a student, view all records, search by roll number, edit a record, and delete a record. It validates required fields, keeps roll numbers unique, and restricts marks and attendance to the range 0–100.

The current version is intended as a small academic demonstration. It does not provide user accounts, role-based permissions, cloud hosting, or multi-user database coordination.

## Target users

- Students demonstrating a database-backed web application.
- A teacher or administrator maintaining a small set of student records locally.

## High-level features

1. Student record creation and input validation.
2. Student listing and roll-number search.
3. Student record update and deletion.
4. SQLite persistence for student details.
