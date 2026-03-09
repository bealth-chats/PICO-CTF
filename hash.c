#include <stdio.h>
#include <stdint.h>
#include <string.h>

uint64_t hash(const char* str) {
    uint64_t h = 0x1505;
    while (*str) {
        h = (h << 5) + h + (uint8_t)*str;
        str++;
    }
    return h;
}

int main() {
    printf("%lu\n", hash("iUbh81!j*hn!"));
    return 0;
}
