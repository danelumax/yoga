/*
 * AddressServer.h
 *
 *  Created on: Aug 28, 2016
 *      Author: eliwech
 */

#ifndef ADDRESSSERVER_H_
#define ADDRESSSERVER_H_

#include "UserDataHandler.h"

class AddressServer {
public:
	virtual ~AddressServer();
	static AddressServer* getInstance();
	static void destory();
	void init();
	void run();
private:
	AddressServer();
	static AddressServer* _instance;
	UserDataHandler* _handler;
	std::string _order, _key, _search_key;
};

#endif /* ADDRESSSERVER_H_ */
