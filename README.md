## Adabiyya Smart Connect – Django ERP (MVP)

This is a Django-based ERP + public website for **Adabiyya Modern Academy Educational & Charitable Society**.

### Apps and Architecture

- **accounts**: Custom `User` model with role-based access (Admin, Staff, Student, Parent, Sponsor, Committee).
- **admissions**: Online admission applications and document uploads.
- **academics**: Classes, students, attendance, exams, results.
- **payments**: Fees and donations with Razorpay integration skeleton.
- **sponsorship**: Sponsor profiles and student sponsorship allocations.
- **committee**: Finance reports, project status, and meeting minutes.
- **core**: Shared models (academic year, institution, CMS pages, notifications) and public website pages.

### Quick Setup

**Database Configuration:**
- By default, the app uses **SQLite** for development (no setup required).
- To use **PostgreSQL** (recommended for production), set environment variable `USE_POSTGRES=True` and configure PostgreSQL credentials.

1. **For PostgreSQL** (optional - skip if using SQLite):
   - Create and configure a PostgreSQL database:
     - **DB name**: `adabiyya`
     - **User**: `adabiyya`
     - **Password**: `adabiyya`
   - Set environment variable: `USE_POSTGRES=True`

2. Create and activate a virtual environment, then install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables (optional for development, required for production):

- `USE_POSTGRES` (set to `True` to use PostgreSQL, default: `False` uses SQLite)
- `DJANGO_SECRET_KEY` (default: dev key, change in production)
- `DJANGO_DEBUG` (default: `True`)
- `DJANGO_ALLOWED_HOSTS` (comma-separated)
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT` (only if `USE_POSTGRES=True`)
- `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`
- Email and SMS settings as needed.

4. Run migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

### Deployment Notes (Gunicorn + Nginx)

- Use `gunicorn adabiyya_smart_connect.wsgi:application` behind Nginx.
- Configure Nginx to:
  - Proxy `location /` to Gunicorn.
  - Serve `/static/` from the `staticfiles` directory (after `python manage.py collectstatic`).
  - Serve `/media/` from the `media` directory.
- Run with `DEBUG=False` and a strong `DJANGO_SECRET_KEY`.


