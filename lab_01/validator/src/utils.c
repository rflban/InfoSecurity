#include "utils.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <ifaddrs.h>
#include <netpacket/packet.h>

#define MIN(a,b) (((a)<(b))?(a):(b))

int is_virtual_if(struct ifaddrs *ifa)
{
    if (!ifa)
        return 0;

    int bit_sum = 0;
    struct sockaddr_ll *sa = (struct sockaddr_ll *)ifa->ifa_addr;

    for (int idx = 0; idx < sa->sll_halen; ++idx)
        bit_sum |= sa->sll_addr[idx];

    return bit_sum == 0;
}

struct mac_addrs *get_mac_addrs()
{
    struct mac_addrs *maddrs = NULL;
    struct mac_addrs *ma;

    struct sockaddr_ll *sa = NULL;
    struct ifaddrs *ifaddr = NULL;
    struct ifaddrs *ifa = NULL;

    if (getifaddrs(&ifaddr) != 0)
    {
        perror("getifaddrs");
        exit(1);
    }

    maddrs = (struct mac_addrs *)malloc(sizeof(struct mac_addrs));

    for (ma = maddrs, ifa = ifaddr; ifa; ifa = ifa->ifa_next)
    {
        if (ifa->ifa_addr &&
            ifa->ifa_addr->sa_family == AF_PACKET &&
            !is_virtual_if(ifa))
        {
            ma->next = (struct mac_addrs *)malloc(sizeof(struct mac_addrs));
            ma = ma->next;
            sa = (struct sockaddr_ll *)ifa->ifa_addr;

            ma->next = NULL;
            ma->alen = sa->sll_halen; 
            strncpy((char *)ma->addr,
                    (const char *)sa->sll_addr,
                    sizeof(ma->addr));
            strncpy(ma->ifa_name,
                    (const char *)ifa->ifa_name,
                    sizeof(ma->ifa_name));
        }
    }

    ma = maddrs;
    maddrs = maddrs->next;

    free(ma);
    freeifaddrs(ifaddr);

    return maddrs;
}

void free_mac_addrs(struct mac_addrs *maddrs)
{
    struct mac_addrs *to_delete;

    while (maddrs)
    {
        to_delete = maddrs;
        maddrs = maddrs->next;

        free(to_delete);
    }
}
