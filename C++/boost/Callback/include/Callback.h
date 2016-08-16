/*
 * Callback.h
 *
 *  Created on: Aug 16, 2016
 *      Author: eliwech
 */

#ifndef CALLBACK_H_
#define CALLBACK_H_

#include <string>
#include <iostream>

/* Callback class should be a singleton, it will not generate a new obj for bind function. */
class Callback
{
public:
	virtual ~Callback();
	static Callback* getInstance();
	void CallbackFunNonParam();
	void CallbackFunOneParam(std::string param);
	std::string CallbackFunTwoParamWithReturn(std::string paramA, std::string paramB);
private:
	Callback();
	static Callback* _instance;
};

#endif /* CALLBACK_H_ */
