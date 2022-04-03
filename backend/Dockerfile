FROM python:3.8

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app

RUN pip install poetry

COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

EXPOSE 8000

CMD ["python","-u", "givemetheodds/main.py"]
