/*
 * Impl.h
 *
 *  Created on: Oct 5, 2016
 *      Author: eliwech
 */

#ifndef IMPL_H_
#define IMPL_H_

#include "Api.h"

class Impl : public Api
{
public:
	Impl();
	virtual ~Impl();
	virtual void test1(std::string s);
};

#endif /* IMPL_H_ */
