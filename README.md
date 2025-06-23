# 🏠 Property Dekho - Real Estate Project

**A feature-rich Real Estate web application built with Python Django and MySQL.**  
This project allows users to browse, list, and manage real estate properties. Integrated with **CKEditor** for rich-text editing in admin.

---

## 🚀 Features

- User registration and authentication
- Property listings with images and descriptions
- Advanced filtering and search functionality
- CKEditor-powered content fields
- Admin dashboard for managing properties and categories
- SEO-friendly property URLs
- Responsive UI with Bootstrap
- MySQL as the database backend

---

## 🛠️ Tech Stack

- **Backend**: Django (Python 3.x)
- **Frontend**: HTML5, CSS3, Bootstrap
- **Database**: MySQL
- **Editor**: CKEditor
- **Others**: Pillow for image handling

---

## ⚙️ MySQL Configuration

1. **Create a MySQL database and user:**

```sql
CREATE DATABASE propertydekho_db CHARACTER SET UTF8MB4;
CREATE USER 'propertyuser'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON propertydekho_db.* TO 'propertyuser'@'localhost';
FLUSH PRIVILEGES;
