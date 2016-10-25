/*
 * Proxy.h
 *
 *  Created on: Oct 23, 2016
 *      Author: eliwech
 */

#ifndef PROXY_H_
#define PROXY_H_

#include "UserModel.h"
#include <boost/xpressive/xpressive_dynamic.hpp>
#include <boost/format.hpp>
#include <boost/tokenizer.hpp>
#include <boost/algorithm/string.hpp>
#include <fstream>

class Proxy : public UserModelApi
{
public:
	Proxy(UserModelApi* realSubject);
	virtual ~Proxy();
    virtual std::string getDepId();
    virtual std::string getName();
    virtual std::string getUserId();
    virtual void setDepId(std::string depId);
    virtual void setName(std::string name);
    virtual void setUserId(std::string userId);
private:
    void reload();
    UserModelApi* _realSubject;
    bool _loaded;
};

#endif /* PROXY_H_ */
