/*
 * OpenCommand.cpp
 *
 *  Created on: Oct 31, 2016
 *      Author: eliwech
 */

#include "OpenCommand.h"

OpenCommand::OpenCommand(MainBoardApi* mainBoard)
	:_mainBoard(mainBoard)
{
}

OpenCommand::~OpenCommand()
{
}

void OpenCommand::execute()
{
	_mainBoard->open();
}
