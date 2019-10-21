FROM python:3.7
COPY requirements.txt ./
EXPOSE 80
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]