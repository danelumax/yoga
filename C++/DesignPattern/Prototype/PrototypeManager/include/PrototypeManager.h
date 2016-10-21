/*
 * PrototypeManager.h
 *
 *  Created on: Oct 21, 2016
 *      Author: eliwech
 */

#ifndef PROTOTYPEMANAGER_H_
#define PROTOTYPEMANAGER_H_

#include <map>
#include "Prototype.h"

class PrototypeManager
{
public:
	virtual ~PrototypeManager();
	static PrototypeManager* getInstance();
	static void destory();
	void setPrototype(std::string prototypeId, Prototype* prototype);
	void removePrototype(std::string prototypeId);
	Prototype* getPrototype(std::string prototypeId);
private:
	PrototypeManager();
	std::map<std::string, Prototype*> _map;
	static PrototypeManager* _instance;
};

#endif /* PROTOTYPEMANAGER_H_ */
