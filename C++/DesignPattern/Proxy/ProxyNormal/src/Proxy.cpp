/*
 * Proxy.cpp
 *
 *  Created on: Oct 23, 2016
 *      Author: eliwech
 */

#include "Proxy.h"

typedef boost::tokenizer< boost::char_separator<char> > CustomTokenizer;

Proxy::Proxy(UserModelApi* realSubject)
	: _realSubject(realSubject), _loaded(false)
{
}

Proxy::~Proxy()
{
}

std::string Proxy::getDepId()
{
	if (!_loaded)
	{
		reload();
		_loaded = true;
	}
    return _realSubject->getDepId();
}

std::string Proxy::getName()
{
    return _realSubject->getName();
}

std::string Proxy::getUserId()
{
    return _realSubject->getUserId();
}

void Proxy::setDepId(std::string depId)
{
    _realSubject->setDepId(depId);
}

void Proxy::setName(std::string name)
{
    _realSubject->setName(name);
}

void Proxy::setUserId(std::string userId)
{
    _realSubject->setUserId(userId);
}

void Proxy::reload()
{
	std::string userId("");
	std::string userName("");
	std::string depId("");
    std::ifstream fin;
    fin.open("data.txt",std::ios::in);
    if(fin)
    {
        fin>>std::noskipws;
        std::string oneLine;

        while(getline(fin, oneLine, '\n'))
        {
            boost::char_separator<char> sep(" ");
            CustomTokenizer tok(oneLine, sep);
            CustomTokenizer::iterator iter = tok.begin();

            userId = *(iter++);
            userName = *(iter++);
            depId = *(iter++);
            if (userId == _realSubject->getUserId())
            {
            	/* just add one attribute into _realSubject */
            	_realSubject->setDepId(depId);
            	break;
            }
            else
            {
            	continue;
            }
        }
    }

    fin.close();
}
