# VAXtheSAT

## Mission overview
Your mission is to hijack a satellite by pointing it to *34.916944*, *-117.376667*, an abandoned USAF radio station in the middle of the desert.

You have obtained access to a client machine in the ground station, which conveniently has a post-it note on it with the following useful information:

```
login: root
Password: vaxthesat!
```

## Network configuration
Machines in the base station communicate through an internal network. You own a client machine on this network, but you need to connect to the server that actually communicates with the satellite.

```
.--.                 .--.                                     }-O-{
|__| .--------.      |__| .--------.      ,--..Y   ) ) )       [^]
|=.| |.------.|      |=.| |.------.|      \   /`.        _____/o o\_____
|--| ||CLIENT|| <--> |--| ||SERVER|| <-->  \.    \      ^""""":{o}:"""""^
|  | |'------'|      |  | |'------'|       |"""--'             /.\
|__|~')______('      |__|~')______('       / \                 \_/
     10.0.0.21            10.0.0.20
```

There is a client program on the client machine. Just type ***client***.

## Resources
Ressources are available on the client machine in the directory ***/root/client/***

You have obtained the server disassembly from a trustworthy source: [link to server.s].

