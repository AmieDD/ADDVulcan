From: Pat Murphy <"TUCVAX::PMURPHY"@NRAO.EDU>
Sender: dishfits-request@fits.CX.NRAO.EDU
To: dishfits@fits.CX.NRAO.EDU
Subject: IEEE-VAX floating conversion
Date: Tue,  7 Nov 89 15:46:44 EDT

With the near-certain imminent approval of the IEEE floating point
format for binary FITS data by the IAU, many observatories will want to
implement FITS writers and/or readers on VAX/VMS or VAX/UNIX machines
that can read IEEE floating point numbers and convert them to native VAX
format, and vice versa.  While it is possible to just multiply/divide by
4.0, this practice is NOT general enough to handle all cases.  In
particular, the IEEE format includes extensions with no counterpart in
the VAX Format such as plus or minus infinity and not-a-number (NaN).
Even worse, it allows negative zero which causes a fatal reserved
operand fault on a VAX. 

I have written a pair of routines that will convert one or more IEEE
floating point numbers to native VAX format and vice versa.  The
IEEE-to-VAX routine detect all the above cases and produce a sensible
result without causing any fatal errors.  They have been tested for
normal data, plus or minus "not-a-number", and plus or minus infinity.
They currently write an indefinite value (defined in the source as
1.6E38) in place of these IEEE exceptional numbers.  The source code
(in C) for these functions is appended to this message; details of 
calling sequences are given in the precursor comments.  The modules
have been tested in both VAX C (V2.4) and GNU C (V1.22) and appear to 
work in either, although I could not get the INDEF constant in Gnu C to
set correctly (this can be fixed by using a regular variable instead).

One nice feature of these modules is that they incorporate word and/or
byte swapping, invoked by flags set in the calling sequence.  Depending
on how you got your data onto a VAX, you may have to swap bytes and/or
(16-bit) words.  See the comments for details, but if in doubt, write
some test data and try the various combinations before committing
yourself.

I can't promise to support this routine or vouch that it's error-free;
however, my testing indicates that it seems to work fine for my test
data.  If you do find a geniune error, however, please let me know.

				- Pat Murphy
                                  ________________
==================================| 12-m Radio   |==============================
| Patrick P. Murphy              / Telescope on  | Internet: PMurphy@nrao.edu  |
| Scientific Programming Analyst | Kitt Peak, AZ | Bitnet:   PMurphy@NRAO      |
| Nat'l Radio Astronomy Obsvty.  \               | Span/Hep: 6654::PMurphy     |
| 949 N. Cherry, Campus Bldg. 65  |              | UU:  uunet!nrao.edu!pmurphy |
| Tucson, AZ 85721-0655           /       Tucson | Phone:   (602) 882-8250     |
=================================/         *     |==============================
                                 |______ ^12m/KP |
                                        \---------

8<8<8<8<8<8<8<8<----------- cut here ------------>8>8>8>8>8>8>8>8
/* IEEEFLT -- convert IEEE floating-point format to or from DEC/VAX format
 *
 * =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
 * Copyright ) 1989 by Patrick P. Murphy and the National Radio Astronomy
 *   Observatory.  This software is freely distributable and may be copied
 *   with only the following restrictions:
 *
 *      1.  This copyright notice must appear EXACTLY as it appears here
 *          in all copies;
 *      2.  The software CANNOT be sold for commercial gain, and the only
 *          charge made in distributing is restricted to a reasonable fee
 *          (if any) to cover handling and materials;
 *      3.  If object code (e.g. object files or object modules in a library)
 *          based on any of these modules is copied or distributed, the
 *          source code with this notice must accompany this object code.
 *
 *   This software is made available AS IS with NO EXPRESS OR IMPLIED WARRANTY 
 *   of any kind.  While Patrick P. Murphy and the National Radio Astronomy
 *   Observatory cannot provide any support for this software, we would
 *   like to hear of any errors in the code.  If you find any errors, please
 *   report them to:  Patrick P. Murphy, NRAO, 949 N. Cherry Avenue, Campus
 *   Building 65, Tucson, AZ 85721-0655, USA; or send e-mail to any of these
 *   addresses: pmurphy@nrao.edu, pmurphy@nrao.bitnet, nrao::pmurphy (on
 *   SPAN or HEPNET, nrao=6654), or ...uunet!nrao.edu!pmurphy.
 * =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
 *
 * There are two functions in this module: ieee2vax and vax2ieee for single
 * precision. They are capable of converting a 32-bit ANSI/IEEE-754 floating-
 * point number or numbers to standard VAX 32-bit F-floating format, and vice 
 * versa.
 *
 * These routines are intended for use on a VAX that has imported IEEE data.
 * It is NOT yet general enough for use anywhere.  In particular, on big-
 * endian machines (like Suns), the order of the mantissa, exponent,
 * and sign in the union structure should be reversed.  
 *
 * The calling sequence is:
 *
 *	(void) ieee2vax (data, &nreals, &wswap, &bswap)
 *	float *data;
 *	int *nreals, *wswap, *bswap;
 *
 * or, from fortran: (*** always use variables, NOT constants or parameters!)
 *
 *	CALL IEEE2VAX (DATA, NREALS, WSWAP, BSWAP)
 *	REAL DATA(*)
 *	INTEGER NREALS, WSWAP, BSWAP
 *
 * and the calling sequence for vax2ieee is identical.  The conversion is
 * done IN PLACE.  
 *
 * This module includes optional byte/word swapping.  A VAX word looks like:
 *
 *       ---------------------------------------------
 *       | s | exponent      | mantissa              | :A (byte address)
 *       |-------------------------------------------|
 *       |                mantissa                   | :A+2 
 *       ---------------------------------------------
 *
 * and values read in, e.g. from a National Instruments GPIB bus will in
 * general need to be word-swapped.  However, data read from a byte stream,
 * e.g. data read in image mode across a TCP/IP network FTP link, will not
 * have to be word swapped but will need byte-swapped.  Same for tape data.
 *
 * I have not tested the conversion of denormalized numbers.
 *----------------------------------------------------------------------
 * Created  May 1989 by Pat Murphy, NRAO/Tucson
 * Modified Oct 1989 by Pat Murphy: do it right, check for NaN, Inf, etc.
 * Modified Oct 1989 by Pat Murphy: Add VAX2IEEE as well.
 * Modified Nov 1989 by Pat Murphy: prevent reserved operand fault (use
 *                                   integer instead of real)
 */

#define INDEF 1.6e38		/* or whatever you want it to be */

  union fstruc {
	unsigned long int longword;
	short int words[2];			/* for swapping */
	char bytes[4];				/* ditto */
	float flt;	       			/* raw number */
	struct {				/* disassemble floating # */
		unsigned int mant1:7;		/* top part of fraction */
		unsigned int exponent:8;	/* Exponent with bias */
		unsigned int sign:1;		/* sign bit */
		unsigned int mant2:16;		/* other part of fraction */
		} f;
	} ;

void ieee2vax (buf, nreals, wswap, bswap)
  unsigned long int *buf;
  int *nreals, *wswap, *bswap;	/* pointers so Fortran calling possible */

{
  float temp;
  int	i;
  short int itemp;		/* for swapping words */
  char ctemp;			/* for swapping bytes */
  union fstruc ieee;

/* ================================================ */

	if (*nreals < 1) 
	    return;

	for (i=0; i<*nreals; i++) {
	    ieee.longword = buf[i];	/* Use int (flt can cause fault) */

	    if (*bswap == 1) {
      	        ctemp = ieee.bytes[0];		/* byte swap (4 bytes) */
	        ieee.bytes[0] = ieee.bytes[1];
	        ieee.bytes[1] = ctemp;
      	        ctemp = ieee.bytes[2];
	        ieee.bytes[2] = ieee.bytes[3];
	        ieee.bytes[3] = ctemp;
	    }
	    if (*wswap == 1) {
	    	itemp = ieee.words[0];		/* word swap */
	    	ieee.words[0] = ieee.words[1];
      	    	ieee.words[1] = itemp;
	    }

/* let's check for NaN, Infinity, negative zero... */

	    if (ieee.f.exponent == 255) 	/* NaN or Infinity. */
		ieee.flt = INDEF;		/*  don't care about sign */
	    else if (ieee.f.exponent == 0)	/* Zap negative zero, causes */
		if ((ieee.f.mant1 == 0) &&	/*  reserved operand fault on */
		    (ieee.f.mant2 == 0))	/*  a VAX (i.e. disregard */
		    ieee.flt = 0.0;		/*  sign on +/- zero) */
		else				/* Denormalized IEEE number */
		    ieee.flt = ieee.flt * 2;	/*  has exponent of -126 (??) */
	    else {				/* Regular number */
		if (ieee.f.exponent > 254)	/*  make sure exponent won't */
		    ieee.flt = INDEF;		/*  overflow */
	    	else {				/*  add 2 to exponent */
		    ieee.flt = ieee.flt * 4;	/*  (VAX has different bias) */
		}
            }
	    buf[i] = ieee.longword;		/* put VAX value back */
	}
}

void vax2ieee(buf, nreals, wswap, bswap)
  float *buf;
  int *nreals, *wswap, *bswap; /* pointers so Fortran calling possible */
{
  float temp;
  int	i;
  short int itemp;		/* for swapping words */
  char ctemp;			/* for swapping bytes */
  union fstruc vaxf;

/* ================================================ */

	if (*nreals < 1) 
	    return;

	for (i=0; i<*nreals; i++) {
	    vaxf.flt = buf[i];

	    if (vaxf.f.exponent < 3) 		/* prevent underflow */
	    	temp = 0.0;
	    else                                                         
		temp = (vaxf.flt / 4.0); 	/* shift exponent by 2 */

		if (*bswap == 1) {		/* byte swap needed */
	     	    ctemp = vaxf.bytes[0];
	    	    vaxf.bytes[0] = vaxf.bytes[1];
	    	    vaxf.bytes[1] = ctemp;
      	    	    ctemp = vaxf.bytes[2];
	    	    vaxf.bytes[2] = vaxf.bytes[3];
	    	    vaxf.bytes[3] = ctemp;
		}
		if (*wswap == 1) {		/* word swap needed */
		    itemp = vaxf.words[0];
		    vaxf.words[0] = vaxf.words[1];
	      	    vaxf.words[1] = itemp;
		}
	    buf[i] = temp;			/* put IEEE value back */
	}
}
                                   



