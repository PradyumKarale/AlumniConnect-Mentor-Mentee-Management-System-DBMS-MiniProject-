# 🚀 AlumniConnect – Mentor–Mentee Management System

> A full-stack web application that connects students with alumni for mentorship, guidance, and structured interaction.

---

## 📌 Project Overview

**AlumniConnect** is a role-based mentor–mentee platform designed to bridge the gap between students and alumni.
It enables students to discover alumni, request mentorship, attend sessions, and provide feedback — all within a structured workflow.

---

## ✨ Key Features

* 🔐 **Secure Authentication**

  * Login/Register with password hashing
  * Session-based authentication

* 👥 **Role-Based Access**

  * Student Dashboard
  * Alumni Dashboard

* 🎓 **Alumni Discovery**

  * Browse alumni profiles
  * Filter by skills

* 📩 **Mentorship Requests**

  * Send, approve, reject requests
  * Status tracking (Pending / Approved / Rejected)

* 📅 **Automatic Session Scheduling**

  * Sessions created when request is approved

* ⭐ **Feedback System**

  * Rating (1–5)
  * Comments after sessions

* 🔔 **Smart UI/UX**

  * Flash messages (no page break)
  * Disabled buttons after actions
  * Clean Bootstrap interface

---

## 🛠 Tech Stack

| Layer    | Technology                  |
| -------- | --------------------------- |
| Backend  | Flask (Python)              |
| Database | MySQL                       |
| Frontend | HTML, Bootstrap             |
| Auth     | Flask Sessions              |
| Security | Password Hashing (Werkzeug) |

---

## 🗄 Database Design

Normalized relational schema with the following tables:

* `users` (student / alumni)
* `requests` (mentorship requests)
* `sessions` (scheduled sessions)
* `feedback` (ratings & comments)
* `skills` (skill list)
* `user_skills` (mapping)

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/PradyumKarale/AlumniConnect-Mentor-Mentee-Management-System-DBMS-MiniProject-.git
cd AlumniConnect-Mentor-Mentee-Management-System-DBMS-MiniProject-
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Setup MySQL Database

```sql
CREATE DATABASE alumni_connect;
USE alumni_connect;
```

👉 Run:

```
schema.sql
```

---

### 5️⃣ Run the Application

```bash
python app.py
```

👉 Open:

```
http://127.0.0.1:5000
```

---

## 📷 Screenshots

* Login Page
<img width="1914" height="1022" alt="Screenshot 2026-03-28 023439" src="https://github.com/user-attachments/assets/1f8c236a-4241-48d9-bc01-661311ad59f3" />
<img width="1919" height="1031" alt="Screenshot 2026-03-28 023446" src="https://github.com/user-attachments/assets/9fa4fad2-999b-4cf3-82af-fce97656da5c" />


* Student Dashboard
<img width="1919" height="1031" alt="Screenshot 2026-03-28 023456" src="https://github.com/user-attachments/assets/3ce33be3-d979-427e-a883-ad4e89afd85e" />

* Alumni Dashboard
<img width="1919" height="1079" alt="Screenshot 2026-03-28 011814" src="https://github.com/user-attachments/assets/d41a9405-fced-4176-a1dc-d909b569f2b5" />
<img width="1919" height="1079" alt="Screenshot 2026-03-28 015159" src="https://github.com/user-attachments/assets/611f8f02-f6a5-44d7-b514-804af0e3c365" />

* Sessions & Feedback
<img width="1919" height="1079" alt="Screenshot 2026-03-28 015639" src="https://github.com/user-attachments/assets/194990e0-7f7a-46d8-b8ae-ebff3b4e04aa" />
<img width="1919" height="1079" alt="Screenshot 2026-03-28 024645" src="https://github.com/user-attachments/assets/26752fd5-8253-4ca9-90ab-fc926e554cb9" />

---

## 🔐 Security Features

* Password hashing using Werkzeug
* Session-based authentication
* Role-based authorization
* SQL injection prevention (parameterized queries)

---

## ⚡ Challenges Solved

* Prevented duplicate session creation
* Fixed transaction conflicts (MySQL)
* Improved UX using flash messages instead of redirects
* Handled duplicate email errors gracefully
* Dynamic UI based on role and status

---

## 🚀 Future Enhancements

* 💬 Real-time chat system
* 📧 Email notifications
* 🎥 Video call integration
* 📊 Admin dashboard & analytics
* 🔎 Advanced search & recommendations

---

## 📁 Project Structure

```
alumni_connect/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── alumni_dashboard.html
│   ├── sessions.html
│
├── app.py
├── schema.sql
├── requirements.txt
├── README.md
```

---

## 🧠 Learning Outcomes

* Full-stack web development with Flask
* Database design & normalization
* SQL joins and transactions
* Authentication & session handling
* UI/UX improvements using Bootstrap

---

## 👨‍💻 Author

**Pradyum Karale**

(🎓 B.Tech CSE – MIT World Peace University, Pune)

---

> 🚀 This project demonstrates real-world backend logic, database design, and full-stack integration.
