/*
 * AddressServer.cpp
 *
 *  Created on: Aug 28, 2016
 *      Author: eliwech
 */

#include "AddressServer.h"

AddressServer* AddressServer::_instance = NULL;

AddressServer::AddressServer()
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

void AddressServer::init()
{
    _handler->InitUserDataList();
    _handler->Print();
}

void AddressServer::run()
{
	std::string order, key, search_key;
    //input order command
    while(order != "!quit")
    {
        std::cout<<"Please input command:"<<std::endl;
        std::cin>>order;
        if(order == "add")
        {
            _handler->InsertUserData();
            std::cout<<"address entry added"<<std::endl;
            _handler->WriteFile();
        }
        else if(order == "search")
        {
            std::cout<<"by (name|mobile|address):";
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
        else if(order == "delete")
        {
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
        else if(order == "listall")
            _handler->Print();
        else if(order == "help")
            _handler->ShowHelp();
        else if(order == "quit")
            break;
        else
            _handler->ShowHelp();
    }
}
