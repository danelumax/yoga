//============================================================================
// Name        : Callback.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <iostream>
#include <Client.h>
#include <Callback.h>
#include <boost/bind.hpp>

int main(void)
{
	Callback* cbObj = Callback::getInstance();
	/* register callback function */
	Client* client = new Client(boost::bind(&Callback::CallbackFunNonParam, cbObj),
								boost::bind(&Callback::CallbackFunOneParam, cbObj, _1),
								boost::bind(&Callback::CallbackFunTwoParamWithReturn, cbObj, _1, _2));
	client->showCallbackNonParam();
	client->showCallbackOneParam("message");
	std::string tmp = client->showCallbackTwoParamWithReturn("hello", "world");
	std::cout << " * Show callback return: " << tmp << std::endl;
	return 0;
}
