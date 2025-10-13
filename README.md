# ICT Record Management System

The ICT Record Management System is a secure and structured internal tool built for managing repair records within the ICT Department of {confidential}. It enables authorized ICT personnel to log repair activities, send confirmation emails to departments, receive feedback and lock records securely once confirmed, reducing impersonation risks, tampering and data mismanagement.

---

## Table of Contents

- [Features](#features)
- [Folder Structure](#folder-structure)
- [System Design](#system-design)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Environment Variables](#environment-variables)
- [Fixtures](#fixtures)
- [Tech Stack](#tech-stack)
- [Project Report](#project-report)
- [Contribution](#contribution)
- [Author](#author)

---

## Features

- **Secure Authentication:** Ensures only authorized ICT personnel can access the system.
- **Role-Based Account Management:** Accounts are managed by the Head of Hardware, with surnames used as default passwords for simplicity.
- **Email Confirmation:** Automatically sends confirmation emails to departments after each repair is logged.
- **Departmental Feedback:** Departments can provide feedback and confirmation through secure, unique links.
- **Record Locking:** Records are locked to prevent tampering or edits after a department confirms the repair.
- **Staff Notifications:** Assigned ICT staff receive a notification once a department completes the confirmation process.
- **Structured Workflow:** A clean and structured record flow prevents impersonation or unauthorized access.

---

## Folder Structure

```
.
├── Document
│   └── report.md
├── README.md
├── base
│   ├── fixtures/
│   ├── templates/
│   ├── utils/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── config/
├── templates/
├── theme/
├── manage.py
├── db.sqlite3
└── requirements.txt
```

-   `base/` – Core app containing models, views, forms, URLs, utilities (emails), templates, and fixtures.
-   `config/` – Django project settings and entry points (ASGI/WSGI).
-   `theme/` – Tailwind CSS integration and static assets.
-   `templates/` – Shared templates for the site and emails.
-   `Document/report.md` – Full project planning and reasoning documentation.

---

## System Design

This system was designed after identifying key problems in the department's existing workflow:

-   Impersonation risks from open complaint logging.
-   No proper confirmation or feedback system.
-   Unclear access levels and tampering risks.

The solution integrates authentication, role-based account management, and email-based confirmations to make the process secure, traceable, and efficient.

See `Document/report.md` for a detailed explanation of the design process.

---

## Installation

1.  **Clone the repository**

    ```bash
    git clone https://github.com/your-username/ict-record-manager.git
    cd ict-record-manager
    ```

2.  **Create and activate a virtual environment**

    ```bash
    # Create the virtual environment
    python -m venv venv

    # Activate on macOS/Linux
    source venv/bin/activate

    # Activate on Windows
    venv\Scripts\activate
    ```

3.  **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

---

## Running the Project

1.  **Apply migrations**

    ```bash
    python manage.py migrate
    ```

2.  **Load fixtures (optional)**
    This will load sample data into your database.
    ```bash
    python manage.py loaddata base/fixtures/repair_records.json
    ```

3.  **Run the development server**

    ```bash
    python manage.py runserver
    ```

Access the site at [http://localhost:8000](http://localhost:8000).

---

## Environment Variables

Create a `.env` file in the project root with the following variables. Update them with your actual credentials for email confirmations to work.

```env
DEBUG=True
SECRET_KEY=your-super-secret-key-here
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password
EMAIL_USE_TLS=True
```

---

## Fixtures

The project includes sample data to help with testing and development:

-   `base/fixtures/repair_records.json` – Sample data for testing the system with pre-loaded records.

---

## Tech Stack

-   **Backend:** Django 5
-   **Frontend:** Django Templates, Tailwind CSS
-   **Email:** SMTP with Django's Email Backend
-   **Utilities:** `django-htmx`, `django-browser-reload`
-   **Database:** SQLite (can be switched to PostgreSQL or others)

---

## Project Report

The full report explaining the planning, challenges and solution design can be found in:
`Document/report.md`

---

## Contribution

This project was built for internal departmental use, but contributions for improvements are welcome. Feel free to fork the repository and open a pull request.

---

## Author

-   **Taiye Babatunde**
-   [Portfolio](https://babatunde-taiye.fly.dev/) | [Email](mailto:taiyebabatundejames@gmail.com)
```