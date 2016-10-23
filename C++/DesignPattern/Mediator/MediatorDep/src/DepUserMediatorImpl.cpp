/*
 * DepUserMediatorImpl.cpp
 *
 *  Created on: Oct 22, 2016
 *      Author: eliwech
 */

#include "DepUserMediatorImpl.h"

DepUserMediatorImpl* DepUserMediatorImpl::_instance = NULL;

DepUserMediatorImpl::DepUserMediatorImpl()
{
	initTestData();
}

DepUserMediatorImpl::~DepUserMediatorImpl()
{
}

DepUserMediatorImpl* DepUserMediatorImpl::getInstance()
{
	if (NULL == _instance)
	{
		_instance = new DepUserMediatorImpl();
	}

	return _instance;
}

void DepUserMediatorImpl::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
	}
}

void DepUserMediatorImpl::initTestData()
{
	DepUserModel* du1 = new DepUserModel();
	du1->setDepUserId("du1");
	du1->setDepId("d1");
	du1->setUserId("u1");
	_depUserVec.push_back(du1);

	DepUserModel* du2 = new DepUserModel();
	du2->setDepUserId("du2");
	du2->setDepId("d1");
	du2->setUserId("u2");
	_depUserVec.push_back(du2);

	DepUserModel* du3 = new DepUserModel();
	du3->setDepUserId("du3");
	du3->setDepId("d2");
	du3->setUserId("u3");
	_depUserVec.push_back(du3);

	DepUserModel* du4 = new DepUserModel();
	du4->setDepUserId("du4");
	du4->setDepId("d2");
	du4->setUserId("u4");
	_depUserVec.push_back(du4);

	DepUserModel* du5 = new DepUserModel();
	du5->setDepUserId("du5");
	du5->setDepId("d2");
	du5->setUserId("u1");
	_depUserVec.push_back(du5);
}

void DepUserMediatorImpl::deleteDep(std::string depId)
{
	std::vector<DepUserModel*>::iterator iter= _depUserVec.begin();
	for(; iter!=_depUserVec.end(); ++iter)
	{
		if ((*iter)->getDepId() == depId)
		{
			_depUserVec.erase(iter);
			iter = _depUserVec.begin();
		}
	}
}

void DepUserMediatorImpl::deleteUser(std::string userId)
{
	std::vector<DepUserModel*>::iterator iter= _depUserVec.begin();
	for(; iter!=_depUserVec.end(); ++iter)
	{
		if ((*iter)->getUserId() == userId)
		{
			_depUserVec.erase(iter);
			iter = _depUserVec.begin();
		}
	}
}

/* List all user info of the specified department */
void DepUserMediatorImpl::showDepUsers(Dep* dep)
{
	std::vector<DepUserModel*>::iterator iter= _depUserVec.begin();
	for(; iter!=_depUserVec.end(); ++iter)
	{
		if ((*iter)->getDepId() == dep->getDepId())
		{
			std::cout << "Department Id: " << dep->getDepId()
					  << ", User Id: " << (*iter)->getUserId() << std::endl;
		}
	}
}

/* List all department info of the specified User */
void DepUserMediatorImpl::showUserDeps(User* user)
{
	std::vector<DepUserModel*>::iterator iter= _depUserVec.begin();
	for(; iter!=_depUserVec.end(); ++iter)
	{
		if ((*iter)->getUserId() == user->getUserId())
		{
			std::cout << "User Id: " << user->getUserId()
					  << ", Department Id: " << (*iter)->getDepId() << std::endl;
		}
	}
}
