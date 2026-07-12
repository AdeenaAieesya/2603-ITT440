dockerfile
FROM python:3.9-slim
WORKDIR /app
RUN pip install flask pymysql
COPY monitor.py .
EXPOSE 5000
CMD ["python", "monitor.py"]
