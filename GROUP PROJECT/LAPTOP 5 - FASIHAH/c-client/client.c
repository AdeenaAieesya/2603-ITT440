#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 8083
#define SERVER_IP "127.0.0.1"
#define POINTS_ADDED 3

int main() {
    int sock;
    struct sockaddr_in serv_addr;
    char buffer[1024] = {0};

    printf("[C Client] Starting...\n");
    printf("[C Client] Connecting to server on port %d\n", PORT);
    printf("[C Client] Points added per update: +%d\n", POINTS_ADDED);
    printf("========================================\n\n");
    fflush(stdout);

    while (1) {
        if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
            printf("[C Client] ❌ Socket creation error\n");
            fflush(stdout);
            return 1;
        }

        serv_addr.sin_family = AF_INET;
        serv_addr.sin_port = htons(PORT);

        if (inet_pton(AF_INET, SERVER_IP, &serv_addr.sin_addr) <= 0) {
            printf("[C Client] ❌ Invalid address\n");
            fflush(stdout);
            return 1;
        }

        if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
            printf("[C Client] ⏳ Waiting for server...\n");
            fflush(stdout);
            close(sock);
            sleep(2);
            continue;
        }

        char *msg = "PING";
        send(sock, msg, strlen(msg), 0);
        printf("[C Client] 📤 Sent: %s\n", msg);
        fflush(stdout);

        int valread = read(sock, buffer, 1024);
        if (valread > 0) {
            buffer[valread] = '\0';
            printf("[C Client] 📥 Server response: %s\n", buffer);
            printf("[C Client] ✅ +%d points added to database!\n", POINTS_ADDED);
            fflush(stdout);
        } else {
            printf("[C Client] ❌ No response from server\n");
            fflush(stdout);
        }

        close(sock);
        printf("========================================\n\n");
        fflush(stdout);
        sleep(30);
    }

    return 0;
}
