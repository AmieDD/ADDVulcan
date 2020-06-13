# Vax the Sat

## Ground Segment

*304 points, 6 solves*

Active ADDVulcan players:

- Bun
- ameer
- shipcod3
- Jigo

# Challenge Description

It's still the 70's in my ground station network, login to it and see if you can get a flag from it.

### Ticket

Present this ticket when connecting to the challenge:

```
ticket{foxtrot41690papa:___a bunch of unguessable stuff___}
```

Don't share your ticket with other teams.

### Connecting

Connect to the challenge on
```
vax.satellitesabove.me:5035
```

Using netcat, you might run
```
nc vax.satellitesabove.me 5035
```

### Files

You'll need these files to solve the challenge.

[Download Files](https://generated.2020.hackasat.com/vaxthesat/vaxthesat-foxtrot41690papa.tar.bz2)
[Download Files](https://static.2020.hackasat.com/2282d39c1d30b59739733d5f0751a2c81e080796/VAXtheSAT.zip)

### Solving

Your team's flag for this challenge will look something like ``` flag{foxtrot41690papa:___a bunch of unguessable stuff___} ``` .

# Solution
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
