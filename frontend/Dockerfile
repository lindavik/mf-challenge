FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY static ./static
COPY ui.py .

EXPOSE 8501

CMD ["streamlit", "run", "ui.py"]