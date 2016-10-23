/*
 * Dep.cpp
 *
 *  Created on: Oct 22, 2016
 *      Author: eliwech
 */

#include "Dep.h"
#include "DepUserMediatorImpl.h"

Dep::Dep()
{
}

Dep::~Dep()
{
}

std::string Dep::getDepId() const
{
    return _depId;
}

std::string Dep::getDepName() const
{
    return _depName;
}

void Dep::setDepId(std::string depId)
{
    _depId = depId;
}

void Dep::setDepName(std::string depName)
{
    _depName = depName;
}

void Dep::deleteDep()
{
	DepUserMediatorImpl* mediator = DepUserMediatorImpl::getInstance();
	mediator->deleteDep(_depId);
}
