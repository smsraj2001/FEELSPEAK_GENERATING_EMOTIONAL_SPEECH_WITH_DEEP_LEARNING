#ifndef _flint_h_
#define _flint_h_
/*
 * flint.h
 *
 * Copyright (C) 2016,2022 Paul Boersma, Johnny Ip, Toni Gojani
 * version 2022-08-22
 *
 * This code is part of OpenVokaturi.
 *
 * OpenVokaturi is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or (at
 * your option) any later version.
 *
 * OpenVokaturi is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software. If not, see http://www.gnu.org/licenses/.
 */

#include <stdint.h>
#include <math.h>

#if defined (__APPLE__) || defined (_WIN64) || defined (__linux__) && ! defined (RASPBERRY_PI)
	#define flint_64BIT  1
#else
	#define flint_64BIT  0
#endif

/*
	For real-time applications you need big integers: with a sampling
	frequency of 44100 Hz, the number of recorded samples will exceed
	the maximum 32-bit signed integer after only 13.5 hours. Therefore,
	having int64_t would be best, and that is indeed what Praat uses for
	these same purposes, but the Vokaturi library has to be able to run with
	old compilers and linkers. Not all old compilers support int64_t, and
	not all old linkers support 64-bit division without calling external
	functions. So we simply employ the type "double", which can contain
	signed integers up to 54 bits.
*/
#if flint_64BIT
	typedef int64_t flint;
#else
	typedef double flint;
#endif
/*
	On these high-precision "integers",
	the integer division (with its rounding down) and the modulo function
	cannot be performed with the usual operator symbols for integer types
	(which are "/" and "%", respectively),
	so for those operations we use inline functions instead.
*/
inline static double real_mod (double a, double b) { return a - floor (a / b) * b; }
#if flint_64BIT
	inline static flint flint_div (flint a, flint b) { return a / b; }
	inline static flint flint_mod (flint a, flint b) { return a % b; }
#else
	inline static flint flint_div (flint a, flint b) { return floor (a / b); }
	inline static flint flint_mod (flint a, flint b) { return real_mod (a, b); }
#endif

/* End of file flint.h */
#endif
