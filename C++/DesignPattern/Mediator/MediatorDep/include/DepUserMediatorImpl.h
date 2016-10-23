/*
 * DepUserMediatorImpl.h
 *
 *  Created on: Oct 22, 2016
 *      Author: eliwech
 */

#ifndef DEPUSERMEDIATORIMPL_H_
#define DEPUSERMEDIATORIMPL_H_

#include <vector>
#include <iostream>
#include "Dep.h"
#include "User.h"
#include "DepUserModel.h"

class DepUserMediatorImpl
{
public:
	virtual ~DepUserMediatorImpl();
	static DepUserMediatorImpl* getInstance();
	static void destory();
	void deleteDep(std::string depId);
	void deleteUser(std::string userId);
	void showDepUsers(Dep* dep);
	void showUserDeps(User* user);
private:
	DepUserMediatorImpl();
	void initTestData();
	static DepUserMediatorImpl* _instance;
	std::vector<DepUserModel*> _depUserVec;
};

#endif /* DEPUSERMEDIATORIMPL_H_ */
