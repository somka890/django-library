# 📚 Django Library

This is a simple **Django-based library system** that allows users to browse books, see details, register/login, and manage personal reading status.  

🚀 Live Demo: [Open App](https://knygu-katalogas.onrender.com)  

---

## ✨ Features
- 👤 User authentication (login, logout, register)  
- 📖 Book catalog with covers & descriptions  
- ⭐ Rating system for books  
- 🏠 User profile with saved data  
- 🎨 Responsive frontend (HTML + CSS)  

---

## 🛠️ Technologies Used
- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS  
- **Database:** SQLite (default, included in repo)  
- **Deployment:** Render (Gunicorn + Whitenoise)  

---

## 📂 Project Structure
core/              # Main Django project
libraryapp/        # Application with models, views, templates
media/covers/      # Book cover images
requirements.txt   # Dependencies
Procfile           # Render deployment config

---

⚡ How to Run Locally
# Clone repository
git clone https://github.com/somka890/django-library.git
cd django-library/core

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start dev server
python manage.py runserver
