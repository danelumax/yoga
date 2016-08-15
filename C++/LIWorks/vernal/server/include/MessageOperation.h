/*
 * MessageOperation.h
 *
 *  Created on: 2016年2月10日
 *      Author: root
 */

#ifndef VERNAL_SERVER_MESSAGEOPERATION_H_
#define VERNAL_SERVER_MESSAGEOPERATION_H_

#include <iostream>
#include <string>
#include "StringUtil.h"

class MessageOperation {
public:
	MessageOperation();
	virtual ~MessageOperation();
	void dothing(std::string message);
private:
};

#endif /* VERNAL_SERVER_MESSAGEOPERATION_H_ */
