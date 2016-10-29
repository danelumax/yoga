/*
 * Newspaper.h
 *
 *  Created on: Oct 27, 2016
 *      Author: eliwech
 */

#ifndef NEWSPAPER_H_
#define NEWSPAPER_H_

#include "Subject.h"

class Newspaper : public Subject
{
public:
	Newspaper();
	virtual ~Newspaper();
	std::string getContent();
	void setContent(std::string content);
private:
	std::string _content;
};

#endif /* NEWSPAPER_H_ */
