/*
 * Message.cpp
 *
 *  Created on: Sep 4, 2016
 *      Author: eliwech
 */

#include "Message.h"

Message::Message(uint32_t appId, uint32_t code)
	:_appId(appId), _code(code)
{
}

Message::~Message()
{
}

uint32_t Message::getAppId() const
{
    return _appId;
}

uint32_t Message::getCode() const
{
    return _code;
}

void Message::setAppId(uint32_t appId)
{
    _appId = appId;
}

void Message::setCode(uint32_t code)
{
    _code = code;
}
