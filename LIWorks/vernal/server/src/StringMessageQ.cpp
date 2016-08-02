/*
 * StringMessageQ.cpp
 *
 *  Created on: 2016年2月12日
 *      Author: root
 */

#include "StringMessageQ.h"

StringMessageQ* StringMessageQ::_instance = NULL;

StringMessageQ::StringMessageQ()
{
	_msgQ = NULL;
}

StringMessageQ::~StringMessageQ() {
	// TODO Auto-generated destructor stub
}

StringMessageQ* StringMessageQ::getInstance()
{
	if(_instance == NULL)
	{
		_instance = new StringMessageQ();
	}

	return _instance;
}

MessageQ* StringMessageQ::getmsgQ()
{
	return _msgQ;
}

int StringMessageQ::initMessageQueue()
{
    _msgQ = new MessageQ();

    if(NULL == _msgQ)
    {
        return -1;
    }

    return 0;
}
