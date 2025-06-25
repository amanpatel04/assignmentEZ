# 🔐 Secure File Sharing System

A Django-based REST API application to securely manage file sharing between two different types of users — **Ops Users** and **Client Users** — with role-based access control and encrypted file URLs.

---

## 📌 Features

### ✅ Ops User
- Login
- Upload files (only `.pptx`, `.docx`, `.xlsx`)
- File type validation and secure storage

### ✅ Client User
- Sign Up (returns **encrypted email verification URL**)
- Login
- List all uploaded files
- Download file via **secure, encrypted link**
- Download links are **accessible only to Client Users**

---

## 🔐 Security Highlights
- JWT-based authentication
- Bcrypt hashed passwords
- Encrypted download URLs (non-shareable and user-restricted)
- Role-based access control

---

## ⚙️ Tech Stack

| Technology     | Usage                       |
|----------------|-----------------------------|
| **Django**     | Web framework (backend)     |
| **Django REST Framework** | API development         |
| **SQLite3** / PostgreSQL | Database (configurable) |
| **bcrypt**     | Secure password hashing     |
| **PyJWT**      | Token-based authentication  |
| **uuid**       | User and file identification|

---

## 📮 API Overview

| Endpoint                    | Method | Access Level    | Description                                  |
|----------------------------|--------|------------------|----------------------------------------------|
| `/api/v1/user/signup/`     | POST   | Public           | Register a new Client User (returns encrypted verification URL) |
| `/api/v1/user/verify/`     | GET    | Public           | Verifies the Client User via encrypted URL   |
| `/api/v1/user/login/`      | POST   | Public           | Login for both Ops and Client Users          |
| `/api/v1/file/upload/`     | POST   | Ops User only    | Upload `.pptx`, `.docx`, `.xlsx` files       |
| `/api/v1/file/`       | GET    | Client User only | List all uploaded files                      |
| `/api/v1/file/download/`   | GET    | Client User only | Generate secure encrypted download link      |

---

## 🛠️ Setup Instructions

### 1️⃣ Clone the Repository

---
```bash
git clone https://github.com/amanpatel04/assignmentEZ.git
cd assignmentEZ
python -m venv env
pip install -r requirements.txt
cd fileshare
python manage.py migate
python manage.py runserver


