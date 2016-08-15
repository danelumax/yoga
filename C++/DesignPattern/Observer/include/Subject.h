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
	Subject(std::string name):_subjectName(name){};
	virtual ~Subject(){};
	std::string getContent();
	void setContent(std::string);
	void attach(Observer *reader);
	void detach(Observer *reader);
	void notifyObservers();
private:
	std::vector<Observer*> _readers;
	std::string _subjectName;
	std::string _content;

};

#endif /* SUBJECT_H_ */
