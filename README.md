# ☁️ VaultSphere

### Intelligent Cloud File Management & Backup System

VaultSphere is a secure cloud file management platform designed to provide users with a centralized workspace for storing, managing, and backing up their digital files.

The system is built using Flask and SQLite and provides user-specific file management with secure authentication and isolated file storage.

---

## 🚀 Features

### 🔐 User Authentication
- User registration
- Secure password hashing
- User login and logout
- Session-based authentication
- User-specific access control

### 📁 My Files
- Upload files
- View uploaded files
- Search files
- Download files
- Delete files
- File metadata management
- User-specific file ownership

### ☁️ Cloud Workspace
- Centralized file management
- Storage usage tracking
- File organization
- Responsive dashboard

### 💾 Backup System
- File backup management
- Backup history
- File restoration support

### 🔄 Version Management
- File version tracking
- Previous version management
- File recovery

### 🤖 AI Assistant
- Intelligent document assistance
- File analysis
- AI-powered cloud workspace features

---

## 🛠️ Technology Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Font Awesome

### Backend
- Python
- Flask
- Flask-SQLAlchemy

### Database
- SQLite

### Security
- Werkzeug Password Hashing
- Flask Sessions
- User-specific file ownership

---

## 📂 Project Structure

```text
VaultSphere/
│
├── app.py
├── database.py
├── README.md
├── .gitignore
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── file.py
│
├── routes/
│   ├── __init__.py
│   ├── auth_routes.py
│   ├── dashboard_routes.py
│   └── files_routes.py
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── files.html
│   │
│   └── components/
│       └── sidebar.html
│
├── static/
│   └── css/
│       ├── style.css
│       ├── auth.css
│       ├── dashboard.css
│       └── files.css
│
└── instance/
    ├── vaultsphere.db
    └── uploads/