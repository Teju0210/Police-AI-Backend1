# 🚔 Police AI Crime Intelligence Platform

An AI-powered Crime Intelligence Platform designed for **Karnataka State Police (KSP)** to assist law enforcement with crime record management, advanced analytics, geospatial visualization, criminal network analysis, and AI-driven predictive policing.

The platform combines a **FastAPI backend** with an **interactive Crime Analytics Dashboard**, enabling police departments to manage crime records efficiently while gaining actionable intelligence through data visualization and machine learning.

---

# 📌 Project Overview

The Police AI Crime Intelligence Platform consists of two major components:

## 🔹 Backend System
A secure REST API built with **FastAPI**, providing authentication, role-based authorization, and CRUD operations for managing crime-related data.

## 🔹 Crime Analytics Dashboard
A Python-powered analytics engine that transforms crime datasets into interactive dashboards featuring:

- District-wise crime analysis
- Crime hotspot maps
- Criminal relationship networks
- Modus Operandi analysis
- AI-based crime prediction
- Anomaly detection
- Early warning alerts

---

# 🚀 Key Features

## 🔐 Backend

- JWT Authentication
- Role-Based Authorization
- User Management
- FIR Management
- Victim Management
- Accused Management
- Evidence Management
- Police Station Management
- Crime Type Management
- Investigation Status Management
- PostgreSQL Integration
- SQLAlchemy ORM
- Interactive Swagger Documentation

---

## 📊 Crime Analytics Dashboard

### 🌍 District-Level Drill-down

- Interactive district map
- Police station drill-down
- District-wise crime statistics

---

### 🔥 Crime Hotspots

- Geospatial hotspot visualization
- Heatmap of crime concentration
- District incident density

---

### ⏰ Spatiotemporal Analysis

Layer crime data based on:

- Morning
- Afternoon
- Evening
- Night

to identify crime clusters by time.

---

### 👥 Criminal Relationship Network

Interactive graph showing:

- Repeat offenders
- Co-accused relationships
- Criminal network visualization
- Risk scoring

---

### 🕵️ Modus Operandi Analysis

Analyze

- Crime methods
- Cross-jurisdiction offenders
- Repeat criminal behaviour

---

### 📈 Crime Trend Analysis

Interactive charts for

- Monthly trends
- Seasonal trends
- Year-wise crime comparison

---

### 🏘 Socio-Economic Correlation

Correlate crime with

- Literacy
- Urbanization
- Population
- Unemployment

using Pearson correlation.

---

### 🤖 AI Predictive Analytics

Machine Learning powered:

- Crime Forecasting
- District Risk Prediction
- High / Medium / Low Risk Classification

using Random Forest Regression.

---

### 🚨 Anomaly Detection

Isolation Forest detects unusual crime incidents that differ from normal crime patterns.

---

### ⚠ Early Warning System

Automatically identifies districts showing rapidly increasing crime trends.

---

# 🛠 Technology Stack

## Backend

- FastAPI
- Python
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT Authentication
- Passlib
- Uvicorn

---

## Analytics

- Python
- Pandas
- NumPy
- Plotly
- Leaflet.js
- NetworkX
- Scikit-learn
- Random Forest
- Isolation Forest

---

## Frontend Dashboard

- HTML5
- CSS3
- JavaScript
- Plotly.js
- Leaflet Maps
- Vis Network

---

# 📁 Project Structure

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
├── ksp_analytics/
│   ├── 1_generate_data.py
│   ├── 2_build_analytics.py
│   ├── 3_build_dashboard.py
│
├── dashboard_template.html
│
├── data/
│   ├── CaseMaster.csv
│   ├── Victim.csv
│   ├── Accused.csv
│   ├── ArrestSurrender.csv
│   └── DistrictProfile.csv
│
├── output/
│   ├── dashboard.html
│   └── dashboard_data.json
│
├── requirements.txt
├── README.md
└── .env
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/Teju0210/Police-AI-Backend1.git
```

---

## Navigate to Project

```bash
cd Police-AI-Backend1
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶ Running Backend

```bash
uvicorn app.main:app --reload
```

Server:

```
http://127.0.0.1:8000
```

---

# 📖 API Documentation

Swagger

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# ▶ Running Crime Analytics Dashboard

Generate datasets

```bash
python ksp_analytics/1_generate_data.py
```

Build analytics

```bash
python ksp_analytics/2_build_analytics.py
```

Generate dashboard

```bash
python ksp_analytics/3_build_dashboard.py
```

Open

```
output/dashboard.html
```

using your browser or VS Code Live Server.

---

# 📊 Dashboard Capabilities

✔ Interactive KPI Cards

✔ District Drill-down

✔ Crime Hotspots

✔ Incident Density Heatmap

✔ Crime Timeline

✔ Crime Type Distribution

✔ Victim Demographics

✔ Criminal Network Analysis

✔ Repeat Offenders

✔ Risk Scoring

✔ Modus Operandi Analysis

✔ Cross-Jurisdiction Behaviour

✔ Socio-Economic Correlation

✔ AI Crime Forecasting

✔ Isolation Forest Anomaly Detection

✔ Early Warning Alerts

---

# 🔒 Authentication

The backend uses JWT Bearer Authentication.

Login to obtain an access token and authorize requests using

```
Bearer <access_token>
```

---

# 🗄 Database

Database

- PostgreSQL

ORM

- SQLAlchemy

---

# 🔮 Future Enhancements

- Conversational AI Assistant
- RAG-based Crime Search
- Voice Assistant
- Kannada ↔ English Translation
- Face Recognition
- Criminal Profile Generation
- Live CCTV Analytics
- Predictive Policing
- GIS Crime Mapping
- Mobile Officer Application

---

# 👨‍💻 Team

Developed as part of the **Police AI Crime Intelligence Platform** for advanced crime analytics and digital policing.

Backend:
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication

Analytics:
- Python
- Plotly
- Machine Learning
- Network Analysis
- Geospatial Intelligence

---

# 📜 License

This project is intended for educational, research, and police innovation purposes.

---

## ⭐ If you found this project useful, consider giving it a Star!
