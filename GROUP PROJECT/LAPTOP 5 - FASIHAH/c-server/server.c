#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <mariadb/mysql.h>
#include <pthread.h>
#include <time.h>

#define PORT 8083
#define NODE_USER "Fasihah"
#define DB_HOST "192.168.43.248"
#define DB_USER "root"
#define DB_PASS "secretpass"
#define DB_NAME "library_stats"
#define POINTS_ADDED 3

MYSQL *conn;

void* update_points(void* arg) {
    while (1) {
        sleep(30);
        char query[256];
        sprintf(query, "UPDATE segmen_mata SET points = points + %d WHERE user = '%s'", POINTS_ADDED, NODE_USER);
        if (mysql_query(conn, query)) {
            printf("[Error] Update failed: %s\n", mysql_error(conn));
            fflush(stdout);
        } else {
            printf("[Fasihah] ✅ Points updated! +%d\n", POINTS_ADDED);
            fflush(stdout);
        }
    }
    return NULL;
}

int main() {
    printf("[Fasihah] Starting server...\n");
    fflush(stdout);
    printf("[Fasihah] Points added per update: +%d\n", POINTS_ADDED);
    fflush(stdout);

    conn = mysql_init(NULL);
    if (!mysql_real_connect(conn, DB_HOST, DB_USER, DB_PASS, DB_NAME, 3306, NULL, 0)) {
        printf("[Error] DB connection failed: %s\n", mysql_error(conn));
        fflush(stdout);
        return 1;
    }
    printf("[Fasihah] ✅ Connected to database\n");
    fflush(stdout);

    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        return 1;
    }

    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
        perror("setsockopt");
        return 1;
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("bind failed");
        return 1;
    }

    if (listen(server_fd, 3) < 0) {
        perror("listen");
        return 1;
    }

    printf("[Fasihah] C Server listening on port %d\n", PORT);
    fflush(stdout);

    pthread_t thread;
    pthread_create(&thread, NULL, update_points, NULL);

    char buffer[1024] = {0};
    while (1) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            perror("accept");
            continue;
        }
        int valread = read(new_socket, buffer, 1024);
        if (valread > 0) {
            buffer[valread] = '\0';
            printf("[Fasihah] Received: %s\n", buffer);
            fflush(stdout);
            send(new_socket, "OK", 2, 0);
        }
        close(new_socket);
    }

    mysql_close(conn);
    return 0;
}
