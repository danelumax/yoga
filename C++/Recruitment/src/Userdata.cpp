/*
 * Userdata.cpp
 *
 *  Created on: Aug 28, 2016
 *      Author: eliwech
 */

#include "Userdata.h"

Userdata::Userdata() {
	// TODO Auto-generated constructor stub

}

Userdata::~Userdata() {
	// TODO Auto-generated destructor stub
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
