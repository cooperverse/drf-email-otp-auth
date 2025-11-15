drf-email-otp-auth

A secure and modular authentication system built with Django REST Framework that enables user registration with email-based OTP verification, login, and password reset. Designed for production-ready applications that require a reliable email verification workflow.

🔥 Features

🔐 User Registration with Email OTP Verification
Users must verify their email using a One-Time Password.

📧 Email OTP Generation & Validation
Auto-expired, rate-limited, and secure.

🔑 Login Support
Password-based login or OTP-based login (optional).

🔄 Password Reset via Email OTP
Reset password securely using an email OTP.

🧩 Modular & Reusable Code Structure
Easily plug into any DRF project.

🛡️ Security Best Practices

OTP expiration

OTP attempt limit

Hashed password & tokens

Throttling

Validations

🗂️ Tech Stack

Python 3.x

Django 5.x

Django REST Framework

SMTP Email Backend (Gmail / Outlook / Custom SMTP)

SQLite (development) / PostgreSQL (recommended for prod)
