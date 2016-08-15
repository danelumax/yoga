/*
 * Reader.cpp
 *
 *  Created on: Aug 11, 2016
 *      Author: eliwech
 */

#include "Reader.h"

Reader::Reader(std::string name)
	:_name(name)
{
}

void Reader::update(Subject *subject)
{
	/*6. fetch Subject status changing and do something */
	std::cout << _name << " get Newspaper" << ", and content is "
			  << subject->getContent() << std::endl;
}
