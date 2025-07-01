# 📱 Dine In App

A Django-based restaurant management application that allows users to browse food items, manage hotels, handle carts, and more. This app is designed to support both admin and user-facing features including food listings, order placement, and restaurant configuration.

---

## 🛠️ Features

- User Registration & Login (Custom User Model)
- Hotel and Food Management
- Add to Cart / Update Cart Quantity
- Order Placement
- Pagination for food lists
- Middleware for Hotel View Count
- Address Auto-fill based on Pincode
- RESTful APIs using Django REST Framework
- Admin Panel for Managing Hotels and Food Items

---

## 🚀 Tech Stack

- **Backend:** Django 5.2.3
- **Database:** PostgreSQL (or default SQLite for development)
- **API:** Django REST Framework
- **Authentication:** Token-based (customizable)

---

## 📁 Project Structure

dine_in_app/
├── food_api/ # Core logic for hotels, food, orders
├── authenticate/ # User authentication logic
├── utils/ # Reusable utilities and middleware
├── dine_in_app/ # Project settings
├── manage.py
├── requirements.txt
└── README.md


## 🧪 Setup Instructions

### 1. Clone the Repo

- git clone https://github.com/Yuvaraj31v/dine_in_app.git
- cd dine_in_app

### 2. Create & Activate Conda Environment
- conda create --name dinein_env python=3.11
- conda activate dinein_env

### 3. Install Dependencies
- pip install -r requirements.txt

### 4. Run Migrations
- python manage.py runserver

### 5. API Endpoints
- POST /api/register/ – Register User
- POST /api/login/ – Login User
- GET /api/hotels/ – List Hotels
- POST /api/cart/add/ – Add to Cart

🙋‍♂️ Author
Yuvaraj V
Passionate Django Developer | Automation Specialist