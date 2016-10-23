/*
 * User.h
 *
 *  Created on: Oct 22, 2016
 *      Author: eliwech
 */

#ifndef USER_H_
#define USER_H_

#include <string>

class User
{
public:
	User();
	virtual ~User();
    std::string getUserId() const;
    std::string getUserName() const;
    void setUserId(std::string userId);
    void setUserName(std::string userName);
    void dimission();

private:
	std::string _userId;
	std::string _userName;
};

#endif /* USER_H_ */
