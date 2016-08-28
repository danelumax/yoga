/*
 * AddressServer.h
 *
 *  Created on: Aug 28, 2016
 *      Author: eliwech
 */

#ifndef ADDRESSSERVER_H_
#define ADDRESSSERVER_H_

#include <map>
#include <string>
#include "UserDataHandler.h"
#include "OptionState.h"

class AddressServer {
public:
	virtual ~AddressServer();
	static AddressServer* getInstance();
	static void destory();
	static void die(int sig);
	void init();
	void registerState();
	void run();
	int updatePrefix(const std::string order, std::string& prefix);
private:
	AddressServer();
	static AddressServer* _instance;
	UserDataHandler* _handler;
	std::string _prefix;
	std::map<std::string, OptionState*> _stateMap;
	bool _shutDown;
	int _quitCount;
};

#endif /* ADDRESSSERVER_H_ */
