#include <stdio.h>
#include <stdlib.h>
#include <ifaddrs.h>
#include <netpacket/packet.h>

#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include "utils.h"

#define KEY_PATHTO ".local/"
#define KEY_DIRECTORY "infosecurity_lab01/"
#define KEY_FILENAME  "key.bin"

int install();
int uninstall();

int main(int argc, char **argv)
{
    if (argc > 1 && argv[1][0] == 'u')
        return uninstall();
    else
        return install();

    return 0;
}

int install()
{
    struct mac_addrs *maddrs;
    char back[128];
    FILE *key_file;

    getcwd(back, sizeof(back));

    chdir(getenv("HOME"));
    chdir(KEY_PATHTO);
    mkdir(KEY_DIRECTORY, 0777);
    chdir(KEY_DIRECTORY);

    maddrs = get_mac_addrs();
    key_file = fopen(KEY_FILENAME, "w");

    for (int idx = 0; idx < maddrs->alen; ++idx)
        fprintf(key_file, "%x%c",
                maddrs->addr[idx],
                (idx == maddrs->alen - 1 ? '\n' : ':'));

    fclose(key_file);
    free_mac_addrs(maddrs);
    chdir(back);

    return 0;
}

int uninstall()
{
    char back[128];

    getcwd(back, sizeof(back));

    chdir(getenv("HOME"));
    chdir(KEY_PATHTO KEY_DIRECTORY);

    remove(KEY_FILENAME);
    chdir("..");
    rmdir(KEY_DIRECTORY);

    chdir(back);

    return 0;
}
