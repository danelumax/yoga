//============================================================================
// Name        : CommandNormal.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "Box.h"
#include "OpenCommand.h"
#include "GigaMainBoard.h"

int main()
{
	MainBoardApi* mainBoard = new GigaMainBoard();
	Command* openCommand = new OpenCommand(mainBoard);

	Box* box = new Box();
	box->setOpenCommand(openCommand);

	box->openButtonPressed();

	delete box;
	delete openCommand;
	delete mainBoard;

	return 0;
}
