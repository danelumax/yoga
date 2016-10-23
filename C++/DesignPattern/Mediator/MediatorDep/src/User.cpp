/*
 * User.cpp
 *
 *  Created on: Oct 22, 2016
 *      Author: eliwech
 */

#include "User.h"
#include "DepUserMediatorImpl.h"

User::User()
{
}

User::~User()
{
}

std::string User::getUserId() const
{
    return _userId;
}

std::string User::getUserName() const
{
    return _userName;
}

void User::setUserId(std::string userId)
{
    _userId = userId;
}

void User::setUserName(std::string userName)
{
    _userName = userName;
}

void User::dimission()
{
	DepUserMediatorImpl* mediator = DepUserMediatorImpl::getInstance();
	mediator->deleteUser(_userId);
}
