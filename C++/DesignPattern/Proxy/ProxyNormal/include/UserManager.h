/*
 * UserManager.h
 *
 *  Created on: Oct 23, 2016
 *      Author: eliwech
 */

#ifndef USERMANAGER_H_
#define USERMANAGER_H_

#include <vector>
#include "Proxy.h"
#include "UserModel.h"

class UserManager
{
public:
	UserManager();
	virtual ~UserManager();
	std::vector<UserModelApi*> getUserByDepId(std::string depId);
};

#endif /* USERMANAGER_H_ */
