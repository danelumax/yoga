/*
 * ContextPolicyFactory.cpp
 *
 *  Created on: Sep 1, 2016
 *      Author: eliwech
 */

#include "ContextPolicyFactory.h"
#include "ContextPolicy.h"


ContextPolicyFactory* ContextPolicyFactory::_instance = NULL;

ContextPolicyFactory::ContextPolicyFactory()
{
	init();
}

ContextPolicyFactory::~ContextPolicyFactory()
{
}

ContextPolicyFactory* ContextPolicyFactory::getInstance()
{
	if (_instance == NULL)
	{
		_instance = new ContextPolicyFactory();
	}

	return _instance;
}

void ContextPolicyFactory::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}


void ContextPolicyFactory::init()
{
	/* Authentication */
	_ctxPolicyMap[std::make_pair(DIA_APP_ID_SWM, DIA_CMD_CODE_DE)] = ContextPolicyAuth::getInstance();

	/* Authorization */
	_ctxPolicyMap[std::make_pair(DIA_APP_ID_S6B, DIA_CMD_CODE_AA)] = ContextPolicyS6bAuthz::getInstance();
}

ContextPolicy *ContextPolicyFactory::getContextPolicy(const uint32_t appId, const uint32_t cmdCode)
{
	typedef std::map<std::pair<uint32_t, uint32_t>, ContextPolicy*> ContextPolicyMapType;
	ContextPolicyMapType::iterator iter = _ctxPolicyMap.find(std::make_pair(appId, cmdCode));
	if (iter != _ctxPolicyMap.end())
	{
		return iter->second;
	}
	else
	{
		return NULL;
	}
}

