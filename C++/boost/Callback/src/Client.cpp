/*
 * Client.cpp
 *
 *  Created on: Aug 16, 2016
 *      Author: eliwech
 */

#include <string>
#include <boost/function.hpp>


#include "Client.h"

/* store callback function into class' memeber */
Client::Client(CallbackNonParam callbackNonParam,
			   CallbackOneParam callbackOneParam,
			   CallbackTwoParamWithReturn callbackTwoParamWithReturn)
	:_callbackNonParam(callbackNonParam),
	 _callbackOneParam(callbackOneParam),
	 _callbackTwoParamWithReturn(callbackTwoParamWithReturn)
{

}

Client::~Client()
{
}

/* the follow function will call callback */
void Client::showCallbackNonParam()
{
	_callbackNonParam();
}

void Client::showCallbackOneParam(std::string message)
{
	_callbackOneParam(message);
}

std::string Client::showCallbackTwoParamWithReturn(std::string paramA, std::string paramB)
{
	std::string tmp = _callbackTwoParamWithReturn(paramA, paramB);
	return tmp;
}
