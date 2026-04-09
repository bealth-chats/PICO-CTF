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

    // In 1360 (getenv loop):
    memcpy(buf + 0x13a7, "\x31\xc0\x90\x90\x90", 5);
    memcpy(buf + 0x13b6, "\x31\xc0\x90\x90\x90", 5);
    memcpy(buf + 0x13c5, "\x31\xc0\x90\x90\x90", 5);

    // In 1460 (getpid check):
    memcpy(buf + 0x149d, "\xb8\x39\x05\x00\x00", 5); // getpid returns 1337
    memcpy(buf + 0x14ab, "\xb8\x39\x05\x00\x00", 5); // syscall(39) returns 1337

    // Replace mutate (1239) with exit(1) so it fails fast
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

            // PATCH 1300 function at the END (134c) to return seed in eax
            // 1349: 66 85 c0 (test ax, ax) -> 3 bytes
            // 134c: b9 01 00 00 00 (mov ecx, 1) -> 5 bytes
            // 1351: 0f 44 c1 (cmove eax, ecx) -> 3 bytes
            // We can replace 1349 with `mov eax, seed; nop; nop; nop; nop; nop; nop`
            // Total 11 bytes.
            buf[0x1349] = 0xb8;
            buf[0x134a] = s & 0xff;
            buf[0x134b] = (s >> 8) & 0xff;
            buf[0x134c] = 0;
            buf[0x134d] = 0;
            buf[0x134e] = 0x90;
            buf[0x134f] = 0x90;
            buf[0x1350] = 0x90;
            buf[0x1351] = 0x90;
            buf[0x1352] = 0x90;
            buf[0x1353] = 0x90;

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
                if (strstr(out, "SK-CERT")) {
                    printf("\nFound! Seed: 0x%x\n%s\n", s, out);
                    FILE *flag_file = fopen("flag.txt", "w");
                    fprintf(flag_file, "%s", strstr(out, "SK-CERT"));
                    fclose(flag_file);
                    exit(0);
                }
            }
        }
        if (seed % 1024 == 0) {
            printf("Seed: 0x%x\n", seed);
            fflush(stdout);
        }
    }

    return 0;
}
