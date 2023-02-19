FROM python:3.7

WORKDIR /src

COPY requirements.txt /src/
RUN pip install -r requirements.txt

COPY app /src/app/
COPY main.py /src/main.py

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]