#ifndef INFOSECURITY_LAB01_VALIDATOR_UTILS_
#define INFOSECURITY_LAB01_VALIDATOR_UTILS_

struct ifaddrs;

struct mac_addrs
{
    struct mac_addrs *next;

    unsigned char    alen;
    unsigned char    addr[17];

    char             ifa_name[256];
};

int is_virtual_if(struct ifaddrs *ifa);

struct mac_addrs *get_mac_addrs();
void free_mac_addrs(struct mac_addrs *maddrs);

#endif // INFOSECURITY_LAB01_VALIDATOR_UTILS_
