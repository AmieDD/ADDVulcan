# Digital Filters, Meh

Included is the simulation code for the attitude control loop for a satellite in orbit. A code reviewer said I made a pretty big mistake that could allow a star tracker to misbehave. Although my code is flawless, I put in some checks to make sure the star tracker can't misbehave anyways.

Review the simulation I have running to see if a startracker can still mess with my filter. Oh, and I'll be giving you the attitude of the physical system as a quaternion, it would be too much work to figure out where a star tracker is oriented from star coordinates, right?

### Ticket

Present this ticket when connecting to the challenge:
ticket{xray47741golf:GNMa5OxcfnF-P8Gdy05txH7MU1hgS4Ziq76v9izFmvvSoVj5Wxkg5N91VzbvZPdXxQ}
Don't share your ticket with other teams.
Connecting

Connect to the challenge on filter.satellitesabove.me:5014 . Using netcat, you might run nc filter.satellitesabove.me 5014

### Files

You'll need these files to solve the challenge.

    https://static.2020.hackasat.com/fd578f9dee5b5ac45b0717a1c7739606bd27013b/src.tar.gz

### Solving

Your team's flag for this challenge will look something like flag{xray47741golf:___a bunch of unguessable stuff___} .
Flag:


**Google Colab Notes:**
https://colab.research.google.com/drive/1vIBky-zlb0A6oIbq8KPLiUirzdiCcU0w#scrollTo=vrxTLVFDwqmy

![55325bc462b458c5664e111ad60f5aca.png](:/88ba7d92bd7340dc8489073b0c4a4f99)



![650e74e44db31a2420a2507b38ac1310.png](:/cb435ca574914e8a81583d03d2b1957b)


[![Image from Gyazo](https://i.gyazo.com/76ab0492be689a0cef099d1bc96b4902.gif)](https://gyazo.com/76ab0492be689a0cef099d1bc96b4902)

### Quaternion 
Package
Function File: [axis, angle] = q2rot (q)
Function File: [axis, angle, qn] = q2rot (q)
Extract vector/angle form of a unit quaternion q.

**Inputs**

**q**
Unit quaternion describing the rotation. Quaternion q can be a scalar or an array. In the latter case, q is reshaped to a row vector and the return values axis and angle are concatenated horizontally, accordingly.
### Outputs

**axis**
Eigenaxis as a 3-d unit vector [x; y; z]. If input argument q is a quaternion array, axis becomes a matrix where axis(:,i) corresponds to q(i).
**angle**
Rotation angle in radians. The positive direction is determined by the right-hand rule applied to axis. The angle lies in the interval [0, 2*pi]. If input argument q is a quaternion array, angle becomes a row vector where angle(i) corresponds to q(i).
**qn**
Optional output of diagnostic nature. qn = reshape (q, 1, []) or, if needed, qn = reshape (unit (q), 1, []).
**Example**
```
          octave:1> axis = [0; 0; 1]
          axis =
          
             0
             0
             1
          
          octave:2> angle = pi/4
          angle =  0.78540
          octave:3> q = rot2q (axis, angle)
          q = 0.9239 + 0i + 0j + 0.3827k
          octave:4> [vv, th] = q2rot (q)
          vv =
          
             0
             0
             1
          
          th =  0.78540
          octave:5> theta = th*180/pi
          theta =  45.000
          octave:6>
          
```
Package: quaternion

## Notes

Conventional celestial reference system and frame
The celestial reference system is based on a kinematical definition, yielding fixed
axis directions with respect to the distant matter of the universe. The system
is materialized by a celestial reference frame consisting of the precise coordinates
of extragalactic objects, mostly quasars, BL Lacertae (BL Lac) sources and a
few active galactic nuclei (AGNs), on the grounds that these sources are that far
away that their expected proper motions should be negligibly small. The current
positions are known to better than a milliarcsecond, the ultimate accuracy being
primarily limited by the structure instability of the sources in radio wavelengths.
A large amount of imaging data is available at the USNO Radio Reference Frame
Image Database <
1> and at the Bordeaux VLBI Image Database <
2>.
The IAU recommended in 1991 (21st IAU GA, Rec. VII, Resol. A4) that the origin
of the celestial reference system is to be at the barycenter of the solar system
and the directions of the axes should be fixed with respect to the quasars. This
recommendation further stipulates that the celestial reference system should have
its principal plane as close as possible to the mean equator at J2000.0 and that
the origin of this principal plane should be as close as possible to the dynamical
equinox of J2000.0. This system was prepared by the IERS and was adopted by
the IAU General Assembly in 1997 (23rd IAU GA, Resol. B2) under the name
of the International Celestial Reference System (ICRS). It officially replaced the
FK5 system on January 1, 1998, considering that all the conditions set up by the
1991 resolutions were fulfilled, including the availability of the Hipparcos optical
reference frame realizing the ICRS with an accuracy significantly better than the
FK5. Responsibilities for the maintenance of the system, the frame and its link
to the Hipparcos reference frame have been defined by the IAU in 2000 (24th IAU
GA, Resol. B1.1)
