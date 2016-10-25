/*
 * UserModel.h
 *
 *  Created on: Oct 23, 2016
 *      Author: eliwech
 */

#ifndef USERMODEL_H_
#define USERMODEL_H_

#include "UserModelApi.h"

class UserModel : public UserModelApi
{
public:
	UserModel();
	virtual ~UserModel();
    virtual std::string getDepId();
    virtual std::string getName();
    virtual std::string getUserId();
    virtual void setDepId(std::string depId);
    virtual void setName(std::string name);
    virtual void setUserId(std::string userId);

private:
	std::string _userId;
	std::string _name;
	std::string _depId;
};

#endif /* USERMODEL_H_ */
