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

    return type;
}

/* AddState */
AddState::AddState(UserDataHandler *handler)
	: OptionState(handler)
{
}

void AddState::handle()
{
    _handler->InsertUserData();
    std::cout<<"address entry added"<<std::endl;
    _handler->WriteFile();
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

    std::cin>>search_key;
    _handler->SearchUserData(search_key, type);
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
    std::cin>>search_key;

    _handler->DeleteUserData(search_key, type);
    _handler->WriteFile();
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


