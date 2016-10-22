/*
 * CDDriver.h
 *
 *  Created on: Oct 22, 2016
 *      Author: eliwech
 */

#ifndef CDDRIVER_H_
#define CDDRIVER_H_

#include "Colleague.h"

class CDDriver : public Colleague
{
public:
	CDDriver(Mediator *mediator);
	virtual ~CDDriver();
	std::string getData();
	void readCD();
private:
	std::string _data;
};

#endif /* CDDRIVER_H_ */
