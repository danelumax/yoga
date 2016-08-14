/*
 * Newspaper.h
 *
 *  Created on: Aug 12, 2016
 *      Author: eliwech
 */

#ifndef NEWSPAPER_H_
#define NEWSPAPER_H_

#include <string>

class Newspaper : public Subject
{
public:
	Newspaper(std::string name): Subject(name){};
	virtual ~Newspaper(){};
};

#endif /* NEWSPAPER_H_ */
