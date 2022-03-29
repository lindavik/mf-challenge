#todo update base image to alpine or slim
FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

#CMD ["python", "-m", "uvicorn", "app.main:app"]
CMD ["python", "-u", "app/main.py"]
