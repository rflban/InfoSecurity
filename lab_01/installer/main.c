#include <stdio.h>
#include <ifaddrs.h>
#include <netpacket/packet.h>

#include "utils.h"

int main(void)
{
    struct ifaddrs *ifaddr = NULL;

    getifaddrs(&ifaddr);

    printf("%d\n", is_virtual_if(ifaddr));
    printf("%d\n", is_virtual_if(ifaddr->ifa_next));

    freeifaddrs(ifaddr);

    return 0;
}
