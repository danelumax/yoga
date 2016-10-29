/*
 * Newspaper.h
 *
 *  Created on: Aug 11, 2016
 *      Author: eliwech
 */

#ifndef SUBJECT_H_
#define SUBJECT_H_

#include <vector>
#include <string>
#include <iostream>
#include "Observer.h"

/* don't put declaration and definition in one .h file */

class Subject
{
public:
	Subject();
	virtual ~Subject();
	void attach(Observer *reader);
	void detach(Observer *reader);
	void notifyObservers(std::string content);
private:
	std::vector<Observer*> _readers;

};

#endif /* SUBJECT_H_ */
