/*
 * Prototype.h
 *
 *  Created on: Oct 21, 2016
 *      Author: eliwech
 */

#ifndef PROTOTYPE_H_
#define PROTOTYPE_H_

#include <string>
#include <iostream>

class Prototype
{
public:
	virtual Prototype* clone() = 0;
	virtual std::string getName() = 0;
	virtual void setName(std::string name) = 0;
	virtual void toString() = 0;
};

#endif /* PROTOTYPE_H_ */
