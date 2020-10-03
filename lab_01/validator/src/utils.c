#include "utils.h"

#include <ifaddrs.h>
#include <netpacket/packet.h>

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
