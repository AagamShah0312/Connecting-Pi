# Connecting Pie

A Django marketplace for people who want to share skills, learn from others, and earn through useful work.

## Run locally

```powershell
C:/Users/cebc/anaconda3/Scripts/activate
C:/Users/cebc/anaconda3/python.exe -m pip install -r requirements.txt
C:/Users/cebc/anaconda3/python.exe manage.py migrate
C:/Users/cebc/anaconda3/python.exe manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Roles

- **Service provider:** publish skills, see other providers, and accept or decline receptor requests.
- **Service receptor:** discover provider skills and send a request to hire or learn. Receptors are not listed in the provider directory.

## Production deployment

Set `DJANGO_SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, and a PostgreSQL `DATABASE_URL`. Render can be provisioned from `render.yaml`; `Procfile` and `vercel.json` are included for platform-compatible starts.

## Tests

```powershell
C:/Users/cebc/anaconda3/python.exe manage.py test
```
