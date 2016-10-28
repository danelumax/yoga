/*
 * Reader.h
 *
 *  Created on: Aug 11, 2016
 *      Author: eliwech
 */

#ifndef READER_H_
#define READER_H_

#include "Subject.h"
#include "Observer.h"

class Reader : public Observer
{
public:
	Reader();
	virtual ~Reader();
	virtual void update(Subject* subject);
    std::string getName();
    void setName(std::string _name);

private:
	std::string _name;
};

#endif /* READER_H_ */
