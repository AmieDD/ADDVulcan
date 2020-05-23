Track-a-sat
===========

We have obtained access to the control system for a groundstation's satellite antenna. The azimuth and elevation motors are controlled by PWM signals from the controller. Given a satellite and the groundstation's location and time, we need to control the antenna to track the satellite. The motors accept duty cycles between 2457 and 7372, from 0 to 180 degrees. 

Some example control input logs were found on the system. They may be helpful to you to try to reproduce before you take control of the antenna. They seem to be in the format you need to provide. We also obtained a copy of the TLEs in use at this groundstation.

