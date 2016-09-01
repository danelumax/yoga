/*
 * ContextAction.cpp
 *
 *  Created on: Sep 1, 2016
 *      Author: eliwech
 */

#include "ContextAction.h"

ContextAction::ContextAction() {
	// TODO Auto-generated constructor stub

}

ContextAction::~ContextAction() {
	// TODO Auto-generated destructor stub
}

ContextActionDER* ContextActionDER::_instance = NULL;
ContextActionDER* ContextActionDER::getInstance()
{
	if (_instance == NULL)
	{
		_instance = new ContextActionDER();
	}

	return _instance;
}

void ContextActionDER::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}
