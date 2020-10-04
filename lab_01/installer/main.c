#include <stdio.h>
#include <ifaddrs.h>
#include <netpacket/packet.h>

#include "utils.h"

int main(void)
{
    struct mac_addrs *maddrs;

    maddrs = get_mac_addrs();

    for (struct mac_addrs *ma = maddrs; ma; ma = ma->next)
    {
        printf("%s: ", ma->ifa_name);
        
        for (int idx = 0; idx < ma->alen; ++idx)
            printf("%x%c", ma->addr[idx], (idx >= ma->alen-1 ? '\n' : ':'));
    }

    free_mac_addrs(maddrs);

    return 0;
}
