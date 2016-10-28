/*
 * Newspaper.cpp
 *
 *  Created on: Oct 27, 2016
 *      Author: eliwech
 */

#include "Newspaper.h"

Newspaper::Newspaper()
{
	// TODO Auto-generated constructor stub

}

Newspaper::~Newspaper()
{
	// TODO Auto-generated destructor stub
}

std::string Newspaper::getContent()
{
	return _content;
}

void Newspaper::setContent(std::string content)
{
	/*2. change status */
	_content = content;
	/*3. notify */
	notifyObservers();
}
