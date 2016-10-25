/*
 * UserModel.cpp
 *
 *  Created on: Oct 23, 2016
 *      Author: eliwech
 */

#include "UserModel.h"

UserModel::UserModel()
{
}

UserModel::~UserModel()
{
}

std::string UserModel::getDepId()
{
    return _depId;
}

std::string UserModel::getName()
{
    return _name;
}

std::string UserModel::getUserId()
{
    return _userId;
}

void UserModel::setDepId(std::string depId)
{
    _depId = depId;
}

void UserModel::setName(std::string name)
{
    _name = name;
}

void UserModel::setUserId(std::string userId)
{
    _userId = userId;
}
