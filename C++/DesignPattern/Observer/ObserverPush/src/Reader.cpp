/*
 * Reader.cpp
 *
 *  Created on: Aug 11, 2016
 *      Author: eliwech
 */

#include "Reader.h"
#include "Newspaper.h"

Reader::Reader()
{
}

Reader::~Reader()
{
}

std::string Reader::getName()
{
    return _name;
}

void Reader::setName(std::string name)
{
    _name = name;
}

void Reader::update(std::string content)
{
	/*6. fetch Subject status changing and do something */
	std::cout << _name << " has received Newspaper" << ", and read it. The content is === "
			  << content << std::endl;
}
