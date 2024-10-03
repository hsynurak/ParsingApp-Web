FROM python:3.9-slim 
ENV PYTHONBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
#RUN python manage.py collectstatic --noinput
#VOLUME ["/app/db.sqlite3"]
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]