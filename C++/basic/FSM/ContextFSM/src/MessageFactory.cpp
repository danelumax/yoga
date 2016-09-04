/*
 * MessageFactory.cpp
 *
 *  Created on: Sep 4, 2016
 *      Author: eliwech
 */

#include "MessageFactory.h"
#include <DiaCommonCode.h>

MessageFactory* MessageFactory::_instance = NULL;

MessageFactory::MessageFactory()
{
}

MessageFactory::~MessageFactory()
{
}

MessageFactory* MessageFactory::getInstance()
{
	if (_instance == NULL)
	{
		_instance = new MessageFactory();
	}

	return _instance;
}

void MessageFactory::destory()
{
	if (NULL != _instance)
	{
		delete _instance;
		_instance = NULL;
	}
}

Message* MessageFactory::getMessage(std::string type)
{
	std::cout << "\n-----> (" << type << ") Message Coming ----->" << std::endl;
	if ("DER" == type)
	{
		return new Message(DIA_APP_ID_SWM, DIA_CMD_CODE_DE);
	}
	else if ("MAA" == type)
	{
		return new Message(DIA_APP_ID_SWX, DIA_CMD_CODE_MA);
	}
	else if ("SAA" == type)
	{
		return new Message(DIA_APP_ID_SWX, DIA_CMD_CODE_SA);
	}
	else if ("AAR" == type)
	{
		return new Message(DIA_APP_ID_S6B, DIA_CMD_CODE_AA);
	}
	else
	{
		return NULL;
	}
}
