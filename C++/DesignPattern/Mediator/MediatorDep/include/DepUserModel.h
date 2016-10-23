/*
 * DepUserModel.h
 *
 *  Created on: Oct 22, 2016
 *      Author: eliwech
 */

#ifndef DEPUSERMODEL_H_
#define DEPUSERMODEL_H_

#include <string>

class DepUserModel
{
public:
    void setDepId(std::string depId)
    {
        _depId = depId;
    }

    void setDepUserId(std::string depUserId)
    {
        _depUserId = depUserId;
    }

    void setUserId(std::string userId)
    {
        _userId = userId;
    }

    std::string getDepId() const
    {
        return _depId;
    }

    std::string getUserId() const
    {
        return _userId;
    }

private:
	std::string _depUserId;
	std::string _depId;
	std::string _userId;

};

#endif /* DEPUSERMODEL_H_ */
