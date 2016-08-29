/*
 * OptionState.cpp
 *
 *  Created on: Aug 28, 2016
 *      Author: eliwech
 */

#include <iostream>
#include "OptionState.h"

/* OptionState */
OptionState::OptionState(UserDataHandler *handler)
	:_handler(handler)
{
}

OptionState::~OptionState()
{
}

int OptionState::getType()
{
	std::string key;
	int type = 0;
	std::cout << "by (name|mobile|address):";
    std::cin>>key;
    if(key == "name")
    {
        std::cout<<"name:";
        type = Userdata::NAME;
    }
    else if(key == "mobile")
    {
        std::cout<<"mobile:";
        type = Userdata::MOBILE;
    }
    else if(key == "address")
    {
        std::cout<<"address:";
        type = Userdata::ADDRESS;
    }
    else
    {
    	type = Userdata::NOTFOUND;
    }

    return type;
}

/* AddState */
AddState::AddState(UserDataHandler *handler)
	: OptionState(handler)
{
}

void AddState::handle()
{
    if (_handler->InsertUserData() == 0)
    {
    	std::cout<<"address entry added successfully"<<std::endl;
    	_handler->WriteFile();
    }
    else
    {
    	std::cout << "address entry added failed" << std::endl;
    }
}

/* SearchState */
SearchState::SearchState(UserDataHandler *handler)
	: OptionState(handler)
{
}

void SearchState::handle()
{
	std::string search_key;
    int type = getType();

    if (type != Userdata::NOTFOUND)
    {
    	std::cin>>search_key;
    	_handler->SearchUserData(search_key, type);
    }
    else
    {
    	std::cout << "Please type again" << std::endl;
    }
}

/* DeleteState */
DeleteState::DeleteState(UserDataHandler *handler)
	: OptionState(handler)
{
}

void DeleteState::handle()
{
	std::string search_key;
    int type = getType();

    if (type != Userdata::NOTFOUND)
    {
    	std::cin>>search_key;
    	_handler->DeleteUserData(search_key, type);
    	_handler->WriteFile();
    }
    else
    {
    	std::cout << "Please type again" << std::endl;
    }
}

/* ListAllState */
ListAllState::ListAllState(UserDataHandler *handler)
	: OptionState(handler)
{
}

void ListAllState::handle()
{
	_handler->Print();
}

/* HelpState */
HelpState::HelpState(UserDataHandler *handler)
	: OptionState(handler)
{
}

void HelpState::handle()
{
	_handler->ShowHelp();
}

/* QuitState */
QuitState::QuitState(UserDataHandler *handler)
	: OptionState(handler)
{
}

void QuitState::handle()
{
	_exit(0);
}


