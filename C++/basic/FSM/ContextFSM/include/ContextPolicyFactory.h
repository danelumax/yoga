/*
 * ContextPolicyFactory.h
 *
 *  Created on: Sep 1, 2016
 *      Author: eliwech
 */

#ifndef CONTEXTPOLICYFACTORY_H_
#define CONTEXTPOLICYFACTORY_H_

#include <map>
#include <iostream>
#include "DiaCommonCode.h"
#include <ContextPolicy.h>

/* abstract factory */
class ContextPolicyFactory
{
public:
	virtual ~ContextPolicyFactory();
	static ContextPolicyFactory* getInstance();
	static void destory();
	ContextPolicy* getContextPolicy(const uint32_t appId, const uint32_t cmdCode);

private:
	ContextPolicyFactory();
	void init();

private:
	static ContextPolicyFactory* _instance;
	std::map<std::pair<uint32_t, uint32_t>, ContextPolicy*> _ctxPolicyMap;


};

#endif /* CONTEXTPOLICYFACTORY_H_ */
