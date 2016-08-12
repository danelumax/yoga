/*
 * Reader.h
 *
 *  Created on: Aug 11, 2016
 *      Author: eliwech
 */

#ifndef READER_H_
#define READER_H_

#include <string>
#include <iostream>
#include "Subject.h"
#include "Observer.h"

class Reader : public Observer
{
public:
	Reader(std::string name);
	virtual void update(Subject* subject);
private:
	std::string _name;
};

#endif /* READER_H_ */
