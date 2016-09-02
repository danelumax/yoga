/*
 * ContextAction.cpp
 *
 *  Created on: Sep 1, 2016
 *      Author: eliwech
 */

#include "ContextAction.h"
#include "MessageHandler.h"

ContextAction::ContextAction()
{
}

ContextAction::~ContextAction()
{
}

void ContextAction::handleAction(DiaSessionContext* context)
{
	if (NULL != _msgHandler)
	{
		_msgHandler->execute(context);
	}
}

ContextActionDER::ContextActionDER()
{
	_msgHandler = new DERMessageHandler();
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



