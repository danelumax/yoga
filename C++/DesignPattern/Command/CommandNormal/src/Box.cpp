/*
 * Box.cpp
 *
 *  Created on: Oct 31, 2016
 *      Author: eliwech
 */

#include "Box.h"

Box::Box()
	:_openCommand(NULL)
{
}

Box::~Box()
{
}

void Box::setOpenCommand(Command* command)
{
	_openCommand = command;
}

void Box::openButtonPressed()
{
	_openCommand->execute();
}
