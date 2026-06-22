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

    // In 1460 (getpid/ptrace 2):
    memcpy(buf + 0x149d, "\xb8\x39\x05\x00\x00", 5); // mov eax, 1337
    memcpy(buf + 0x14ab, "\xb8\x39\x05\x00\x00", 5); // syscall(39) returns 1337

    // Decoy exits 1
    memcpy(buf + 0x1239, "\x31\xff\x40\xff\xc7\xb8\x3c\x00\x00\x00\x0f\x05", 12);

    char *argv[] = {"beacon", NULL};
    char *envp[] = {NULL};

    // Use a small loop
    int BATCH = 128;
    for (int seed = 0; seed < 65536; seed += BATCH) {
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

            int fd = memfd_create("beacon", MFD_CLOEXEC);
            write(fd, buf, size);

            char path[256];
            sprintf(path, "/proc/self/fd/%d", fd);

            pipe2(pipes[i], O_CLOEXEC);

            pids[i] = fork();
            if (pids[i] == 0) {
                dup2(pipes[i][1], STDOUT_FILENO);
                close(pipes[i][0]);
                execve(path, argv, envp);
                exit(1);
            }
            close(pipes[i][1]);
            close(fd); // Parent closes memfd AFTER execve is guaranteed (or just let it die)
            // Wait, if I close `fd` BEFORE waitpid, does the child lose it?
            // YES, because I used `O_CLOEXEC`?! NO, `execve` with `O_CLOEXEC` closes the fd inside the child!
            // BUT `execve` LOADS the file into memory!
            // So if I close the fd after `fork` and `execve`, is it safe?
            // YES, Linux keeps the inode alive if it's executing!
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

            if (WIFEXITED(status) && WEXITSTATUS(status) == 0 && n > 0) {
                printf("\nFound! Seed: 0x%x\n%s\n", s, out);
                FILE *flag_file = fopen("flag.txt", "w");
                fprintf(flag_file, "%s", strstr(out, "SK-CERT"));
                fclose(flag_file);
                exit(0);
            }
        }
    }

    return 0;
}
