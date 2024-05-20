# Vault Guard

## Introduction

Vault Guard is a secure and user-friendly password management application built using Django. It allows users to store and manage passwords, secure notes, bank accounts, and payment cards securely. The application ensures data security by encrypting sensitive information with a user-defined quick PIN.

## Demo Video

https://github.com/johurul000/vault_guard/assets/90057499/8a7b609b-72e1-45bc-b2a7-b08e16f059b2




## Features

- **Secure Storage**: Safely store passwords, secure notes, bank accounts, and payment cards.
- **Encryption**: Encrypt and decrypt data using a 4-digit quick PIN.
- **User Authentication**: Secure user registration and login system.
- **User-friendly UI**: User-friendly interface with responsive design using HTML, CSS, Tailwind, and JavaScript.
- **Database**: Data is stored securely in a PostgreSQL database.

## Tech Stack

- **Backend**: Django
- **Frontend**: HTML, CSS, Tailwind, JavaScript
- **Database**: PostgreSQL

## Project Setup

### Prerequisites

- Python 3.x
- Django 3.x
- PostgreSQL

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/vault-guard.git
   cd vault-guard
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv env
   source env/bin/activate   # On Windows use `env\Scripts\activate`
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL database**

   Ensure PostgreSQL is installed and running. Create a database and update the `DATABASES` setting in `vault_guard/settings.py`:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'vault_guard_db',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

5. **Apply migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```bash
   python manage.py runserver
   ```

   Open your browser and navigate to `http://127.0.0.1:8000/` to see the application running.

## Usage

### Registration and Login

- **Register**: Users can register by providing a username and password.
- **Login**: After registration, users can log in with their credentials.

### Quick PIN Setup

- **First Login**: Upon first login, users are prompted to set a 4-digit quick PIN.
- **PIN Usage**: This quick PIN is used to encrypt and decrypt sensitive data stored in the application.

### Managing Entries

- **Passwords**: Store and manage passwords for various services.
- **Secure Notes**: Keep important notes secure.
- **Bank Accounts**: Store bank account details safely.
- **Payment Cards**: Manage credit and debit card information securely.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature-branch`)
6. Open a pull request

---

Feel free to open issues for any questions or concerns. Happy coding!
