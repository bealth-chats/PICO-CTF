#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <fcntl.h>
#include <sys/wait.h>
#include <stdint.h>

int main() {
    FILE *f = fopen("beacon", "rb");
    fseek(f, 0, SEEK_END);
    long size = ftell(f);
    fseek(f, 0, SEEK_SET);

    char *buf = malloc(size);
    fread(buf, 1, size, f);
    fclose(f);

    memcpy(buf + 0x1360, "\x31\xc0\xc3", 3);
    memcpy(buf + 0x1460, "\x31\xc0\xc3", 3);
    memcpy(buf + 0x1239, "\x31\xff\x40\xff\xc7\xb8\x3c\x00\x00\x00\x0f\x05", 12);

    char *argv[] = {"beacon", NULL};
    char *envp[] = {NULL};

    int BATCH = 128;
    for (int seed = 0; seed < 65536; seed += BATCH) {
        int fds[BATCH];
        int pipes[BATCH][2];
        pid_t pids[BATCH];

        for (int i = 0; i < BATCH; i++) {
            int s = seed + i;
            if (s >= 65536) break;

            buf[0x1300] = 0xb8;
            buf[0x1301] = s & 0xff;
            buf[0x1302] = (s >> 8) & 0xff;
            buf[0x1303] = 0;
            buf[0x1304] = 0;
            buf[0x1305] = 0xc3;

            fds[i] = memfd_create("beacon", MFD_CLOEXEC);
            write(fds[i], buf, size);

            char path[256];
            sprintf(path, "/proc/self/fd/%d", fds[i]);

            pipe2(pipes[i], O_CLOEXEC);

            pids[i] = fork();
            if (pids[i] == 0) {
                dup2(pipes[i][1], STDOUT_FILENO);
                close(pipes[i][0]);
                execve(path, argv, envp);
                exit(1);
            }
            close(pipes[i][1]);
        }

        for (int i = 0; i < BATCH; i++) {
            int s = seed + i;
            if (s >= 65536) break;

            char out[1024];
            memset(out, 0, 1024);
            int n = read(pipes[i][0], out, sizeof(out)-1);
            close(pipes[i][0]);

            int status;
            waitpid(pids[i], &status, 0);
            close(fds[i]);

            if (WIFEXITED(status) && WEXITSTATUS(status) == 0 && n > 0) {
                // DON'T CHECK FOR "SK-CERT", JUST PRINT ANY EXIT 0 OUTPUT
                printf("\nExited 0! Seed: 0x%x\nOutput:\n%s\n", s, out);
                FILE *flag_file = fopen("flag.txt", "w");
                fprintf(flag_file, "%s", out);
                fclose(flag_file);
                exit(0);
            }
        }
    }

    return 0;
}
