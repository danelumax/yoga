/*
 * UserModelApi.h
 *
 *  Created on: Oct 23, 2016
 *      Author: eliwech
 */

#ifndef USERMODELAPI_H_
#define USERMODELAPI_H_

#include "string"
#include <iostream>

class UserModelApi
{
public:
    virtual std::string getDepId() = 0;
    virtual std::string getName() = 0;
    virtual std::string getUserId() = 0;
    virtual void setDepId(std::string depId) = 0;
    virtual void setName(std::string name) = 0;
    virtual void setUserId(std::string userId) = 0;

};

#endif /* USERMODELAPI_H_ */
