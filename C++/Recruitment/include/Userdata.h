/*
 * Userdata.h
 *
 *  Created on: Aug 28, 2016
 *      Author: eliwech
 */

#ifndef USERDATA_H_
#define USERDATA_H_

#include <string>

class Userdata
{
public:
	enum Flag
	{
		NAME = 1,
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

private:
    std::string _name;
    std::string _mobile;
    std::string _address;
};

#endif /* USERDATA_H_ */
