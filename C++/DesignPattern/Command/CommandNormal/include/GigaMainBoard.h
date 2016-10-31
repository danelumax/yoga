/*
 * GigaMainBoard.h
 *
 *  Created on: Oct 31, 2016
 *      Author: eliwech
 */

#ifndef GIGAMAINBOARD_H_
#define GIGAMAINBOARD_H_

#include "MainBoardApi.h"
#include <iostream>

class GigaMainBoard : public MainBoardApi
{
public:
	GigaMainBoard();
	virtual ~GigaMainBoard();
	virtual void open();
};

#endif /* GIGAMAINBOARD_H_ */
