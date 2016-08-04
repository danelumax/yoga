/*
 * Target.h
 *
 *  Created on: Aug 4, 2016
 *      Author: eliwech
 */

#ifndef TARGET_H_
#define TARGET_H_

#include "Adaptee.h"

class Target
{
public:
	virtual ~Target(){};
	virtual void request() = 0;
};

class Adapter : public Target
{
public:
	Adapter(Adaptee *adaptee);
	virtual ~Adapter(){};
	virtual void request();
private:
	Adaptee *_adaptee;
};

Adapter::Adapter(Adaptee *adaptee)
{
	_adaptee = adaptee;
}

void Adapter::request()
{
	std::cout << "I will use other interface..." << std::endl;
	_adaptee->specificRequest();
}

#endif /* TARGET_H_ */
