# Vax the Sat
Connect: ```nc vax.satellitesabove.me 5035```
Ticket:ticket{foxtrot41690papa:GImHwxb6WA16b1rVdUKJzE2W2UFlPnWZ1P3NXGS97b39Wc6M5_5m6EY3ZUz88BckgQ}


#Solution
- Login to OpenBSD instance: root : vaxthesat!
- Then use the command below to get the flag:

```
client 10.0.0.20
EPS STATE CONFIG
EPS CFG ADCS ON
ADCS STATE CONFIG
ADCS CFG_POS 00000000 00000000 00000000000000000000000000000001
```

Flag: ```flag{foxtrot41690papa:GAZ4K0Ud-sw9tle6VTQcYPxZyyl--D9cZwiDZsb37-4KhMwrMyYaegdW2d0M_TbF2ughodJkkEnnMZPj6RxHHLY```

[Credits to ameer for first solving this one in our team]
