/*
 * Userdata.cpp
 *
 *  Created on: Aug 28, 2016
 *      Author: eliwech
 */

#include "Userdata.h"

Userdata::Userdata()
{
}

Userdata::~Userdata()
{
}

std::string Userdata::getAddress() const
{
    return _address;
}

std::string Userdata::getMobile() const
{
    return _mobile;
}

std::string Userdata::getName() const
{
    return _name;
}

void Userdata::setAddress(std::string address)
{
    _address = address;
}

void Userdata::setMobile(std::string mobile)
{
    _mobile = mobile;
}

void Userdata::setName(std::string name)
{
    _name = name;
}

void Userdata::toString()
{
	std::cout << getName() << " "
			  << getMobile() << " "
			  << getAddress() << std::endl;
}

void Userdata::operator=(const Userdata& userDate)
{
	_name = userDate.getName();
	_mobile = userDate.getMobile();
	_address = userDate.getAddress();
}
