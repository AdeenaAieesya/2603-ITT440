FROM python:3.9-slim
WORKDIR /app
COPY server.py .
RUN pip install pymysql
CMD ["python", "server.py"]
