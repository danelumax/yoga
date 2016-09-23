/*
 * Userdata.h
 *
 *  Created on: Aug 28, 2016
 *      Author: eliwech
 */

#ifndef USERDATA_H_
#define USERDATA_H_

#include <string>
#include <iostream>

class Userdata
{
public:
	enum Flag
	{
		NOTFOUND = 0,
		NAME,
		MOBILE,
		ADDRESS
	};
	Userdata();
	virtual ~Userdata();

    std::string getAddress() const;
    std::string getMobile() const;
    std::string getName() const;
    void setAddress(std::string address);
    void setMobile(std::string mobile);
    void setName(std::string name);
    void toString();
    void operator=(const Userdata& userDate);

private:
    std::string _name;
    std::string _mobile;
    std::string _address;
};

#endif /* USERDATA_H_ */
