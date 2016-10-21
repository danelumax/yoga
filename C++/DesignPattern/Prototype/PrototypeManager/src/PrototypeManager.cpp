/*
 * PrototypeManager.cpp
 *
 *  Created on: Oct 21, 2016
 *      Author: eliwech
 */

#include "PrototypeManager.h"

PrototypeManager* PrototypeManager::_instance = NULL;

PrototypeManager::PrototypeManager()
{
}

PrototypeManager::~PrototypeManager()
{
}

PrototypeManager* PrototypeManager::getInstance()
{
	if (NULL == _instance)
	{
		_instance = new PrototypeManager();
	}

	return _instance;
}

void PrototypeManager::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
	}
}

void PrototypeManager::setPrototype(std::string prototypeId, Prototype* prototype)
{
	_map[prototypeId] = prototype;
}

void PrototypeManager::removePrototype(std::string prototypeId)
{
	std::map<std::string, Prototype*>::iterator iter = _map.find(prototypeId);
	if (iter != _map.end())
	{
		_map.erase(iter);
	}
}

Prototype* PrototypeManager::getPrototype(std::string prototypeId)
{
	std::map<std::string, Prototype*>::iterator iter = _map.find(prototypeId);
	if (iter != _map.end())
	{
		return iter->second;
	}
	else
	{
		std::cout << "The prototype you want to get has not been registered yet or been deleted already ..." << std::endl;
		return NULL;
	}
}
