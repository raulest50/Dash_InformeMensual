FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# Modify CMD to list directory contents and then start the app
CMD ["sh", "-c", "ls -R /app; python app.py"]

#CMD ["python", "app.py"]
