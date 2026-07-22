# 🚔 Police AI Crime Intelligence Platform (Backend)

## 📌 Project Overview

The Police AI Crime Intelligence Platform is a FastAPI-based backend application designed to help police departments manage crime records digitally. It provides secure authentication, role-based access control, and CRUD APIs for managing FIRs, victims, accused persons, evidence, police stations, crime types, and investigation status.

This backend is built for integration with AI modules such as crime analytics, RAG-based search, chatbot assistance, and predictive crime analysis.

---

## 🚀 Features

* JWT Authentication
* Role-Based Authorization
* User Management
* FIR Management
* Victim Management
* Accused Management
* Evidence Management
* Police Station Management
* Crime Type Management
* Investigation Status Management
* PostgreSQL Database
* SQLAlchemy ORM
* Interactive Swagger API Documentation

---

## 🛠️ Technology Stack

* FastAPI
* Python
* PostgreSQL
* SQLAlchemy
* Pydantic
* JWT Authentication
* Passlib (Password Hashing)
* Uvicorn

---

## 📁 Project Structure

```
Police-AI-Backend/
│
├── app/
│   ├── auth/
│   ├── database/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   └── main.py
│
├── requirements.txt
├── README.md
├── .env
└── .gitignore
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project:

```bash
cd Police-AI-Backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

### Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the server:

```bash
uvicorn app.main:app --reload
```

---

## 📖 API Documentation

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

## 📌 Available APIs

* Authentication
* Users
* FIR
* Victims
* Accused
* Evidence
* Police Stations
* Crime Types
* Investigation Status

---

## 🔒 Authentication

The backend uses JWT Bearer Authentication.

Login to obtain an access token, then authorize requests using:

```
Bearer <your_access_token>
```

---

## 📊 Database

Database: PostgreSQL

ORM: SQLAlchemy

---

## 🔮 Future Enhancements

* Crime Analytics Dashboard
* AI Crime Chatbot
* RAG-based Crime Search
* Voice Input/Output
* English ↔ Kannada Translation
* Criminal Profile Generation
* Predictive Crime Analytics

---

## 👨‍💻 Backend Team

Backend developed using FastAPI, PostgreSQL, SQLAlchemy, and JWT Authentication as part of the Police AI Crime Intelligence Platform project.
