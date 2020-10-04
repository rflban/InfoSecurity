#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "utils.h"

#define KEY_PATHTO ".local/"
#define KEY_DIRECTORY "infosecurity_lab01/"
#define KEY_FILENAME  "key.bin"

int true_main(int argc, char **argv);

int main(int argc, char **argv)
{
    char back[128];
    FILE *key_file;
    unsigned char mac[17] = { 0 };
    unsigned char mac_len;

    getcwd(back, sizeof(back));

    chdir(getenv("HOME"));
    chdir(KEY_PATHTO KEY_DIRECTORY);
    key_file = fopen(KEY_FILENAME, "r");
    chdir(back);

    if (!key_file)
    {
        perror("~/" KEY_PATHTO KEY_DIRECTORY KEY_FILENAME);
        exit(1);
    }

    unsigned int tmp;
    for (mac_len = 0; mac_len < 17 && !feof(key_file);)
        if (fscanf(key_file, "%x:", &tmp) == 1)
            mac[mac_len++] = tmp;

    fclose(key_file);

    struct mac_addrs *maddrs = get_mac_addrs();

    for (struct mac_addrs *ma = maddrs; ma; ma = ma->next)
    {
        if (mac_len == ma->alen)
        {
            tmp = strncmp((const char *)maddrs->addr,
                          (const char *)mac, mac_len);

            if (tmp == 0)
            {
                free_mac_addrs(maddrs);
                return true_main(argc, argv);
            }
        }
    }

    free_mac_addrs(maddrs);

    fprintf(stderr, "Key is invalid\n");
    exit(1);
}

int true_main(int argc, char **argv)
{
    printf("Program!\n");

    return 0;
}
