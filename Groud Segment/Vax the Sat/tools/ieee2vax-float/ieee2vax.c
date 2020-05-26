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

/* Code cleaned up and adapted to convert and pretty print the numbers by Piotr Esden-Tempski <piotr@esden.net> in 2020 */

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>

#define INDEF 1.6e38		/* or whatever you want it to be */

union fstruc {
	uint32_t longword;
	uint16_t words[2];			/* for swapping */
	uint8_t bytes[4];				/* ditto */
	float flt;	       			/* raw number */
	struct {				/* disassemble floating # */
		unsigned int mant1:7;		/* top part of fraction */
		unsigned int exponent:8;	/* Exponent with bias */
		unsigned int sign:1;		/* sign bit */
		unsigned int mant2:16;		/* other part of fraction */
	} f;
};

void ieee2vax (uint32_t *buf, int nreals, int wswap, int bswap)
{
	float temp;
	int	i;
	uint16_t itemp;		/* for swapping words */
	uint8_t ctemp;			/* for swapping bytes */
	union fstruc ieee;

	/* ================================================ */

	if (nreals < 1)
		return;

	for (i=0; i<nreals; i++) {
		ieee.longword = buf[i];	/* Use int (flt can cause fault) */

		if (bswap == 1) {
			ctemp = ieee.bytes[0];		/* byte swap (4 bytes) */
			ieee.bytes[0] = ieee.bytes[1];
			ieee.bytes[1] = ctemp;
			ctemp = ieee.bytes[2];
			ieee.bytes[2] = ieee.bytes[3];
			ieee.bytes[3] = ctemp;
		}
		if (wswap == 1) {
			temp = ieee.words[0];		/* word swap */
			ieee.words[0] = ieee.words[1];
			ieee.words[1] = itemp;
		}

		/* let's check for NaN, Infinity, negative zero... */

		if (ieee.f.exponent == 255) 	/* NaN or Infinity. */
			ieee.flt = INDEF;			/*  don't care about sign */
		else if (ieee.f.exponent == 0)	/* Zap negative zero, causes */
			if ((ieee.f.mant1 == 0) &&	/*  reserved operand fault on */
				(ieee.f.mant2 == 0))	/*  a VAX (i.e. disregard */
				ieee.flt = 0.0;			/*  sign on +/- zero) */
			else						/* Denormalized IEEE number */
				ieee.flt = ieee.flt * 2;	/*  has exponent of -126 (??) */
		else {							/* Regular number */
			if (ieee.f.exponent > 254)	/*  make sure exponent won't */
				ieee.flt = INDEF;		/*  overflow */
			else {						/*  add 2 to exponent */
				ieee.flt = ieee.flt * 4;	/*  (VAX has different bias) */
			}
		}
		buf[i] = ieee.longword;			/* put VAX value back */
	}
}

void vax2ieee(float *buf, int nreals, int wswap, int bswap)
{
	float temp;
	int	i;
	short int itemp;		/* for swapping words */
	char ctemp;			/* for swapping bytes */
	union fstruc vaxf;

/* ================================================ */

	if (nreals < 1)
		return;

	for (i=0; i<nreals; i++) {
		vaxf.flt = buf[i];

		if (vaxf.f.exponent < 3)		/* prevent underflow */
			temp = 0.0;
		else
			temp = (vaxf.flt / 4.0); 	/* shift exponent by 2 */

		if (bswap == 1) {				/* byte swap needed */
			ctemp = vaxf.bytes[0];
			vaxf.bytes[0] = vaxf.bytes[1];
			vaxf.bytes[1] = ctemp;
			ctemp = vaxf.bytes[2];
			vaxf.bytes[2] = vaxf.bytes[3];
			vaxf.bytes[3] = ctemp;
		}
		if (wswap == 1) {				/* word swap needed */
			itemp = vaxf.words[0];
			vaxf.words[0] = vaxf.words[1];
			vaxf.words[1] = itemp;
		}
		buf[i] = temp;					/* put IEEE value back */
	}
}

int main(int argc, char *argv[])
{
	if (argc < 2) {
		printf("You need to provide at least one float value as a parameter.\n");
		return 1;
	}

	//printf("input %s %f\n", argv[1], (float)atof(argv[1]));

	float fvalues[1] = {(float)atof(argv[1])};
	uint32_t *ivalues = (uint32_t *)fvalues;

	printf("float input value %f\n", fvalues[0]);
	printf("ieee float binary size in bytes %ld\n", sizeof(ivalues[0]));
	printf("ieee float binary hex   0x%08X\n", ivalues[0]);
	printf("ieee float binary oct 0%011o\n", ivalues[0]);
	printf("ieee float binary dec   %010d\n", ivalues[0]);
	printf("ieee float binary components:\n");
	printf("Sign Bit\n");
	printf(" | Exponent 8bit\n");
	printf(" | |       Fraction 23bit\n");
	printf(" V V        V\n");
	printf(".-.--------.-----------------------.\n");
	// Print the elements in binary
	printf("|%c|", (ivalues[0] & 0x80000000) ? '1' : '0');
	for (int i = 0; i < 8; i++){
		putchar((ivalues[0] & (0x40000000 >> i)) ? '1' : '0');
		//printf("0x%08X\n", 0x40000000 >> i);
	}
	putchar('|');
	for (int i = 0; i < 23; i++){
		putchar((ivalues[0] & (0x00400000 >> i)) ? '1' : '0');
		//printf("0x%08X\n", 0x00400000 >> i);
	}
	printf("| binary\n");
	// Print the elements in hex
	printf("|%c|", (ivalues[0] & 0x80000000) ? '-' : '+');
	printf("    0x%02X|               0x%06X| hex\n", (ivalues[0] & 0x7F800000) >> 23, ivalues[0] & 0x007FFFFF);
	printf("|%c|", (ivalues[0] & 0x80000000) ? '-' : '+');
	printf("     %03d|                %07d| decimal\n", (ivalues[0] & 0x7F800000) >> 23, ivalues[0] & 0x007FFFFF);
	printf("'-'--------'-----------------------'\n");
	// Print the elements in decimal
	printf("31 30     23                      0\n\n");

	ieee2vax(ivalues, 1, 1, 0);

	printf("VAX-11 Floating Point Representation: \"F_Floating\" Structure (32 bit \"longword\"):\n");
	printf("vax F float binary hex   0x%08X\n", ivalues[0]);
	printf("vax F float binary oct 0%011o\n", ivalues[0]);
	printf("vax F float binary dec   %010d\n", ivalues[0]);
	printf("Fraction (second part) 16bit  Fraction (first part) 7bit\n");
	printf(" |            Exponent 8bit    |\n");
	printf(" |         Sign Bit |          |\n");
	printf(" V                V V          V\n");
	printf(".----------------.-.--------.-------.\n");
	// Print the elements in binary
	putchar('|');
	for (int i = 0; i < 16; i++){
		putchar((ivalues[0] & (0x80000000 >> i)) ? '1' : '0');
		//printf("0x%08X\n", 0x80000000 >> i);
	}
	printf("|%c|", (ivalues[0] & 0x00008000) ? '1' : '0');
	for (int i = 0; i < 8; i++){
		putchar((ivalues[0] & (0x00004000 >> i)) ? '1' : '0');
		//printf("0x%08X\n", 0x00004000 >> i);
	}
	putchar('|');
	for (int i = 0; i < 7; i++){
		putchar((ivalues[0] & (0x00000040 >> i)) ? '1' : '0');
		//printf("0x%08X\n", 0x00000040 >> i);
	}
	printf("| binary\n");
	printf("|          0x%04X|%c|    0x%02X|   0x%02X| hex\n", (ivalues[0] & 0xFFFF0000) >> 16,
															   (ivalues[0] & 0x00008000) ? '-' : '+',
															   (ivalues[0] & 0x00007F80) >> 7,
															   ivalues[0] & 0x0000007F);
	printf("|           %05d|%c|     %03d|    %03X| decimal\n", (ivalues[0] & 0xFFFF0000) >> 16,
																(ivalues[0] & 0x00008000) ? '-' : '+',
																(ivalues[0] & 0x00007F80) >> 7,
																ivalues[0] & 0x0000007F);
	printf("'----------------'-'--------'-------'\n");
	printf("31               15 14     7 6     0\n");

	return 0;
}
