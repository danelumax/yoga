/*
 * Impl2.h
 *
 *  Created on: Oct 5, 2016
 *      Author: eliwech
 */

#ifndef IMPL2_H_
#define IMPL2_H_

#include "Api.h"

class Impl2 : public Api
{
public:
	Impl2();
	virtual ~Impl2();
	virtual void test1(std::string s);
};

#endif /* IMPL2_H_ */
