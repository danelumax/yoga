/*
 * Client.h
 *
 *  Created on: Aug 16, 2016
 *      Author: eliwech
 */

#ifndef CLIENT_H_
#define CLIENT_H_

#include <boost/function.hpp>

typedef boost::function<void()> CallbackNonParam;
typedef boost::function<void(std::string)> CallbackOneParam;
typedef boost::function<std::string(std::string, std::string)> CallbackTwoParamWithReturn;

class Client {
public:
	Client(CallbackNonParam callbackNonParam,
		   CallbackOneParam callbackOneParam,
		   CallbackTwoParamWithReturn callbackTwoParamWithReturn);
	virtual ~Client();
	void showCallbackNonParam();
	void showCallbackOneParam(std::string message);
	std::string showCallbackTwoParamWithReturn(std::string paramA, std::string paramB);
private:
	CallbackNonParam _callbackNonParam;
	CallbackOneParam _callbackOneParam;
	CallbackTwoParamWithReturn _callbackTwoParamWithReturn;

};

#endif /* CLIENT_H_ */
