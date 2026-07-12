FROM gcc:latest
RUN apt-get update && apt-get install -y libmariadb-dev
WORKDIR /app
COPY server.c .
RUN gcc server.c -o server -lmariadb -lpthread
EXPOSE 8080
CMD ["./server"]
