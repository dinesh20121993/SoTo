# SoTo — Shopping + Todo Life Organizer

![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.3-black?logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)
![Deployed on Render](https://img.shields.io/badge/Deployed-Render-46E3B7?logo=render&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

> A modular personal productivity web application to organize your life into sections, track goals, and manage shopping lists — all in one place.

🌐 **Live App:** [https://soto-uj32.onrender.com](https://soto-uj32.onrender.com)

---

## 📌 Purpose

SoTo (Shopping + Todo) is built for people who want a single, structured place to manage different areas of their life — whether it's Study, Gym, Work, or Personal errands.

Instead of juggling multiple apps, SoTo lets you:

- Create **custom life sections** (e.g., Study, Gym, Work)
- Track **Goals (Todos)** with deadlines and priorities
- Manage **Shopping Lists** with quantities and estimated costs
- View a **Dashboard** showing your Top 10 priorities at a glance

---

## 🛠️ Technologies Used

| Layer | Technology |
|---|---|
| **Language** | Python 3.14 |
| **Web Framework** | Flask 3.0.3 |
| **ORM** | Flask-SQLAlchemy 3.1.1 |
| **Database** | SQLite (local) / PostgreSQL-ready |
| **Authentication** | Flask-Login 0.6.3 |
| **Templating** | Jinja2 |
| **Password Hashing** | Werkzeug Security |
| **Production Server** | Gunicorn 22.0.0 |
| **Deployment** | Render.com |
| **Version Control** | Git + GitHub |

---

## 📁 Project Structure

```
soto/
│
├── app/
│   ├── __init__.py          # App factory, blueprint registration
│   ├── models.py            # SQLAlchemy models (User, Section, Goal, ShoppingItem)
│   ├── routes/
│   │   ├── auth.py          # Login / Logout
│   │   ├── dashboard.py     # Dashboard — Top 10 Goals & Shopping Items
│   │   ├── sections.py      # Section CRUD
│   │   ├── goals.py         # Goal CRUD
│   │   └── shopping.py      # Shopping Item CRUD
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── section.html
│   │   └── login.html
│   │
│   └── static/
│       ├── css/
│       └── js/
│
├── config.py                # App configuration
├── run.py                   # Entry point
├── requirements.txt         # Python dependencies
└── README.md
```

---

## 🚀 How to Clone the Repository

Make sure you have **Git** and **Python 3.10+** installed on your machine.

```bash
# Clone the repository
git clone https://github.com/dinesh20121993/SoTo.git

# Navigate into the project folder
cd SoTo
```

---

## 💻 How to Run the App Locally

### 1. Create and activate a virtual environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it — macOS/Linux
source venv/bin/activate

# Activate it — Windows
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the application

```bash
python run.py
```

### 4. Open in your browser

```
http://127.0.0.1:5000
```

> **Note:** The SQLite database is created automatically on first run. No additional database setup is required.

---

## 🗄️ Database Models

| Model | Key Fields |
|---|---|
| **User** | id, username, password_hash |
| **Section** | id, name, user_id |
| **Goal** | id, section_id, name, deadline, priority, is_completed |
| **ShoppingItem** | id, section_id, name, quantity, estimated_cost, priority, is_purchased |

**Priority System:** High = 3 · Medium = 2 · Low = 1
**Dashboard sorting:** `ORDER BY priority DESC, deadline ASC`

---

## 🤝 How to Contribute

We welcome contributions! Follow these steps to contribute to the project:

### 1. Fork the repository

Click the **Fork** button at the top right of this page on GitHub.

### 2. Clone your fork

```bash
git clone https://github.com/YOUR_USERNAME/SoTo.git
cd SoTo
```

### 3. Create a new branch for your feature

```bash
git checkout -b feature/your-feature-name
```

> Use descriptive branch names like `feature/add-search-bar` or `fix/login-redirect`

### 4. Make your changes

Edit the code, add your feature, or fix the bug.

### 5. Stage and commit your changes

```bash
git add .
git commit -m "feat: describe what you changed"
```

> **Commit message conventions:**
> - `feat:` — new feature
> - `fix:` — bug fix
> - `docs:` — documentation update
> - `style:` — formatting, no logic change
> - `refactor:` — code restructuring

### 6. Push to your fork

```bash
git push origin feature/your-feature-name
```

### 7. Open a Pull Request

Go to the original repo on GitHub and click **"Compare & pull request"**. Describe your changes clearly.

---

## 🌐 Live Deployment

The app is deployed on **Render** (free tier):

🔗 [https://soto-uj32.onrender.com](https://soto-uj32.onrender.com)

> **Note:** The free tier on Render spins down after inactivity. The first load may take 30–60 seconds to wake up. Subsequent loads are instant.

---

## 📋 Roadmap

- [x] User authentication (login/logout)
- [x] Section management
- [x] Goals with priority and deadline
- [x] Shopping list with cost tracking
- [x] Priority-based dashboard
- [ ] REST API layer (`/api/...` endpoints)
- [ ] PostgreSQL migration
- [ ] User registration (multi-user support)
- [ ] Mobile-responsive UI

---

## 👤 Author

**Dinesh** — [@dinesh20121993](https://github.com/dinesh20121993)

---

## 📄 License

This project is licensed under the MIT License. Feel free to use, modify, and distribute.
