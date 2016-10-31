/*
 * Box.h
 *
 *  Created on: Oct 31, 2016
 *      Author: eliwech
 */

#ifndef BOX_H_
#define BOX_H_

#include "Command.h"
#include <iostream>

class Box
{
public:
	Box();
	virtual ~Box();
	void setOpenCommand(Command* command);
	void openButtonPressed();
private:
	Command* _openCommand;
};

#endif /* BOX_H_ */
