# 1. Asosiy Python versiyasini tanlaymiz
FROM python:3.12.3-slim

# 2. Atrof-muhit o'zgaruvchilari (bular o'zgarmaydi)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Ishchi papka
WORKDIR /app

# 4. Tizim kutubxonalarini o'rnatamiz
RUN apt-get update && apt-get install -y gettext && rm -rf /var/lib/apt/lists/*

# 5. AVVAL faqat talablar fayllarini ko'chiramiz. Bu Docker keshini optimallashtiradi.
COPY requirements/base.txt requirements/production.txt ./requirements/

# 6. PRODUCTION uchun kerakli kutubxonalarni o'rnatamiz
RUN pip install --no-cache-dir -r requirements/production.txt

# 7. Butun loyiha kodini ko'chiramiz
COPY . .

# 8. Static fayllarni bir joyga yig'amiz (whitenoise uchun)
# Bu buyruq `manage.py collectstatic` ni ishga tushiradi
# Va unga QAYSI SOZLAMALAR faylini ishlatishni aytamiz
RUN SECRET_KEY=dummy-key-for-collectstatic DEBUG=False python manage.py collectstatic --noinput --settings=core.settings.production

# 9. Ilovani ishga tushirish buyrug'i (GUNICORN web-serveri orqali)
# BU ENG MUHIM QATOR!
CMD gunicorn core.wsgi:application --bind 0.0.0.0:$PORT --env DJANGO_SETTINGS_MODULE=core.settings.production