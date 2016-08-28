/*
 * OptionState.cpp
 *
 *  Created on: Aug 28, 2016
 *      Author: eliwech
 */

#include <iostream>
#include "OptionState.h"

OptionState::OptionState(UserDataHandler *handler)
	:_handler(handler)
{
	// TODO Auto-generated constructor stub

}

OptionState::~OptionState() {
	// TODO Auto-generated destructor stub
}

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

SearchState::SearchState(UserDataHandler *handler)
	: OptionState(handler)
{
}

void SearchState::handle()
{
	std::string key, search_key;
	std::cout << "by (name|mobile|address):";
    std::cin>>key;
    if(key == "name")
    {
        std::cout<<"name:";
        std::cin>>search_key;
        _handler->SearchUserData(search_key, 1);
    }
    if(key == "mobile")
    {
        std::cout<<"mobile:";
        std::cin>>search_key;
        _handler->SearchUserData(search_key, 2);
    }
    if(key == "address")
    {
        std::cout<<"address:";
        std::cin>>search_key;
        _handler->SearchUserData(search_key, 3);
    }
}

DeleteState::DeleteState(UserDataHandler *handler)
	: OptionState(handler)
{
}

void DeleteState::handle()
{
	std::string key, search_key;
	std::cout<<"by (name|mobile|address):";
    std::cin>>key;
    if(key == "name")
    {
        std::cout<<"name:";
        std::cin>>search_key;
        _handler->DeleteUserData(search_key, 1);
        _handler->WriteFile();
    }
    if(key == "mobile")
    {
        std::cout<<"mobile:";
        std::cin>>search_key;
        _handler->DeleteUserData(search_key, 2);
        _handler->WriteFile();
    }
    if(key == "address")
    {
        std::cout<<"address:";
        std::cin>>search_key;
        _handler->DeleteUserData(search_key, 3);
        _handler->WriteFile();
    }
}

ListAllState::ListAllState(UserDataHandler *handler)
	: OptionState(handler)
{
}

void ListAllState::handle()
{
	_handler->Print();
}

HelpState::HelpState(UserDataHandler *handler)
	: OptionState(handler)
{
}

void HelpState::handle()
{
	_handler->ShowHelp();
}

QuitState::QuitState(UserDataHandler *handler)
	: OptionState(handler)
{
}

void QuitState::handle()
{
	_exit(0);
}


