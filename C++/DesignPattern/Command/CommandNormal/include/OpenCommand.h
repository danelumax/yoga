/*
 * OpenCommand.h
 *
 *  Created on: Oct 31, 2016
 *      Author: eliwech
 */

#ifndef OPENCOMMAND_H_
#define OPENCOMMAND_H_

#include "Command.h"
#include "MainBoardApi.h"

class OpenCommand : public Command
{
public:
	OpenCommand(MainBoardApi* mainBoard);
	virtual ~OpenCommand();
	virtual void execute();
private:
	MainBoardApi* _mainBoard;
};

#endif /* OPENCOMMAND_H_ */
