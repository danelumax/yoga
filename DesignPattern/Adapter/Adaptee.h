/*
 * Adaptee.h
 *
 *  Created on: Aug 4, 2016
 *      Author: eliwech
 */

#ifndef ADAPTEE_H_
#define ADAPTEE_H_

#include <iostream>

class Adaptee
{
public:
	void specificRequest();
};

void Adaptee::specificRequest()
{
	std::cout << "I am in other interface." << std::endl;
}

#endif /* ADAPTEE_H_ */
