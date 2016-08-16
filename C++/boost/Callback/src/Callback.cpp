/*
 * Callback.cpp
 *
 *  Created on: Aug 16, 2016
 *      Author: eliwech
 */

#include "Callback.h"

Callback* Callback::_instance = NULL;
Callback::Callback()
{
}

Callback::~Callback()
{
}

Callback* Callback::getInstance()
{
	if (_instance == NULL)
	{
		_instance = new Callback();
	}

	return _instance;
}

/* the following will be callback to be called by other class */
void Callback::CallbackFunNonParam()
{
	std::cout << " * Call Non Parameter Function back * " << std::endl;
}

void Callback::CallbackFunOneParam(std::string param)
{
	std::cout << " * Call One Parameter Function back, and Show Parameter: \""<< param <<"\" * " << std::endl;
}

std::string Callback::CallbackFunTwoParamWithReturn(std::string paramA, std::string paramB)
{
	std::cout << " * Call Two Parameter Function With Return back, and Show Parameter: \""<< paramA << " " << paramB <<"\" * " << std::endl;
	std::string tmp = paramA + " " + paramB;
	return tmp;
}
