## Django boilerplate

## How to set up project (with Docker)

Give permission to docker script: ```chmod +x ./docker-compose```
Give permission to docker script: ```chmod +x entrypoint.dev.sh```

### Docker compose file
Build and docker up containers: ```docker-compose -f docker-compose.dev.yml up -d --build```

### Use docker-compose file
```./docker-compose makemigrations``` or ```docker-compose -f docker-compose.dev.yml exec backend python manage.py makemigrations```

## How to run project locally bash script (Linux, Mac)

### install requirements

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements/develop.text
```

### create .env file

```bash
cp .env.example .env
```

### create database

```bash
sudo -u postgres psql
CREATE DATABASE django_boilerplate;
CREATE USER django_boilerplate WITH PASSWORD 'django_boilerplate';
ALTER ROLE django_boilerplate SET client_encoding TO 'utf8';
ALTER ROLE django_boilerplate SET default_transaction_isolation TO 'read committed';
ALTER ROLE django_boilerplate SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE django_boilerplate TO django_boilerplate;
\q
```

### set up .env file with your database credentials

```bash
nano .env
```

### run migrations

```bash
python manage.py migrate
```

### run server

```bash
python manage.py runserver
```

## Pre-commit  must be installed for all projects

```bash
pip install pre-commit
pre-commit install
```


# Back-End checklist:
## 1. Environment Configuration:
- [ ] Ensure that the Django project settings are properly configured for the production environment.
- [ ] Set <span style="font-family:&quot;SFMono-Regular&quot;, Menlo, Consolas, &quot;PT Mono&quot;, &quot;Liberation Mono&quot;, Courier, monospace;line-height:normal;background:rgba(135,131,120,.15);color:#EB5757;border-radius:4px;font-size:85%;padding:0.2em 0.4em;font-weight:600" data-token-index="1" spellcheck="false" class="notion-enable-hover">DEBUG</span> to <span style="font-family:&quot;SFMono-Regular&quot;, Menlo, Consolas, &quot;PT Mono&quot;, &quot;Liberation Mono&quot;, Courier, monospace;line-height:normal;background:rgba(135,131,120,.15);color:#EB5757;border-radius:4px;font-size:85%;padding:0.2em 0.4em;font-weight:600" data-token-index="1" spellcheck="false" class="notion-enable-hover">False</span> in the production settings (<span style="font-family:&quot;SFMono-Regular&quot;, Menlo, Consolas, &quot;PT Mono&quot;, &quot;Liberation Mono&quot;, Courier, monospace;line-height:normal;background:rgba(135,131,120,.15);color:#EB5757;border-radius:4px;font-size:85%;padding:0.2em 0.4em;font-weight:600" data-token-index="1" spellcheck="false" class="notion-enable-hover">settings.py</span>).
- [ ] Verify that the <span style="font-family:&quot;SFMono-Regular&quot;, Menlo, Consolas, &quot;PT Mono&quot;, &quot;Liberation Mono&quot;, Courier, monospace;line-height:normal;background:rgba(135,131,120,.15);color:#EB5757;border-radius:4px;font-size:85%;padding:0.2em 0.4em;font-weight:600" data-token-index="1" spellcheck="false" class="notion-enable-hover">ALLOWED_HOSTS</span> setting includes the production domain names or IP addresses.
## 2. Security:
- [ ] Secure sensitive data, such as secret keys and database credentials, by storing them in environment variables or a secure secrets management system.
- [ ] Implement Cross-Site Request Forgery (CSRF) protection.
- [ ] In Login forms google recaptcha is required.
## 3. Database:
- [ ] Check all migrations is correctly created.
- [ ] Optimize database queries for performance.
## 4. Static and Media Files:
- [ ] Collect and compress static files using <span style="font-family:&quot;SFMono-Regular&quot;, Menlo, Consolas, &quot;PT Mono&quot;, &quot;Liberation Mono&quot;, Courier, monospace;line-height:normal;background:rgba(135,131,120,.15);color:#EB5757;border-radius:4px;font-size:85%;padding:0.2em 0.4em;font-weight:600" data-token-index="1" spellcheck="false" class="notion-enable-hover">collectstatic</span> and configure their storage.
- [ ] Handle user-uploaded media files securely and efficiently.
- [ ] Using media compressing.
- [ ] Creating media models for all media.
## 5. Logging and Monitoring:
- [ ] Implement monitoring and alerting using tools like Prometheus, Grafana, Flower, Sentry(must have)
## 6. Performance Optimization:
- [ ] Profile and optimize database queries, views, and templates for performance.(DEBUGTOOLBAR, DJANGO-SILK)
- [ ] Implement caching mechanisms for frequently accessed data. (depends on project)
- [ ] Configure web server settings, such as Gunicorn or Uvicorn, for optimal performance
## 7. Testing:
- [ ] Conduct integration tests, Unit Tests
- [ ] Set up a staging environment that closely mirrors the production environment for testing purposes.(if needed)
## 8. Documentation:
- [ ] Swagger
- [ ] Ensure that the codebase is well-documented, including comments and docstrings  and add doc for apis to swagger.
## 9. Common Coding Requirements:
- [ ] Pre-commit
- [ ] Using right branches like dev, master
- [ ] Search history add (new api)
- [ ] Notification from initial
- [ ] Full Readme (deployment and project set up guide)
- [ ] Docker required for production deployment
## 10. Testing the Production Environment:
- [ ] Conduct load testing to ensure the application can handle expected traffic volumes(Locust.io)
