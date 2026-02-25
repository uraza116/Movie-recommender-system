FROM python:3.13

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python ./model_builder.py

EXPOSE 5000

CMD ["python", "./app.py"]