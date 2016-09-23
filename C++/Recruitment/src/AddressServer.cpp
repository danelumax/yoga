/*
 * AddressServer.cpp
 *
 *  Created on: Aug 28, 2016
 *      Author: eliwech
 */

#include "AddressServer.h"
#include <boost/xpressive/xpressive_dynamic.hpp>
#include <boost/format.hpp>
#include <boost/tokenizer.hpp>
#include <boost/algorithm/string.hpp>
#include "StringUtils.h"
#include <SignalManagement.h>

typedef boost::tokenizer< boost::char_separator<char> > CustomTokenizer;
AddressServer* AddressServer::_instance = NULL;

AddressServer::AddressServer()
	:_prefix("sh"), _shutDown(false), _quitCount(0)
{
	_handler = new UserDataHandler();
}

AddressServer::~AddressServer()
{
}

AddressServer* AddressServer::getInstance()
{
	if (_instance == NULL)
	{
		_instance = new AddressServer();
	}

	return _instance;
}

void AddressServer::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}

void AddressServer::registerState()
{
	_stateMap["add"] = new AddState(_handler);
	_stateMap["search"] = new SearchState(_handler);
	_stateMap["delete"] = new DeleteState(_handler);
	_stateMap["listall"] = new ListAllState(_handler);
	_stateMap["help"] = new HelpState(_handler);
	_stateMap["quit"] = new QuitState(_handler);
	_stateMap["exit"] = new QuitState(_handler);
}

void AddressServer::init()
{
    _handler->InitUserDataList();
    _handler->Print();
    registerState();
}

void AddressServer::run()
{
	std::string order;

	SignalManagement::getInstance()->signal(SIGINT, SignalManagement::KEEP_RUNNING, AddressServer::die);
	/* input order command */
    while(!_shutDown)
    {
        std::cout << _prefix << "> ";
        std::cin >> order;
        /* change Upper to Lower */
        order = StringUtils::toLowerCase(order);
        if(!updatePrefix(order, _prefix))
        {
        	/* state pattern */
        	std::map<std::string, OptionState*>::iterator iter = _stateMap.find(order);
        	if (iter != _stateMap.end())
        	{
        		iter->second->handle();
        	}
        }
    }
}

int AddressServer::updatePrefix(const std::string order, std::string& prefix)
{
	int ret = 0;
	/* string need use sregex, match (.) + (any char) */
	boost::xpressive::sregex reg = boost::xpressive::sregex::compile("\\..*");

	if(boost::xpressive::regex_match(order, reg))
    {
        boost::char_separator<char> sep("/");
        CustomTokenizer tok(order, sep);

        std::vector<std::string> vecSegTag;
        CustomTokenizer::iterator iter = tok.begin();
        /* get second */
      	prefix = *(++iter);
      	ret = 1;
    }

	return ret;
}

void AddressServer::die(int sig)
{
	std::cout << "\nSystem catch Ctrl+C signal, quit Address Server ..." << std::endl;

	SignalManagement::getInstance()->sigDefault(sig);
	_instance->_shutDown = true;

}

