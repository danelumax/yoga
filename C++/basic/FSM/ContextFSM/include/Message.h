/*
 * Message.h
 *
 *  Created on: Sep 4, 2016
 *      Author: eliwech
 */

#ifndef MESSAGE_H_
#define MESSAGE_H_

#include <string>
#include <stdint.h>
#include <iostream>

class Message
{
public:
	Message(uint32_t appId, uint32_t code);
    ~Message();
    uint32_t getAppId() const;
    uint32_t getCode() const;
    void setAppId(uint32_t appId);
    void setCode(uint32_t code);

private:
    uint32_t _appId;
    uint32_t _code;
};

#endif /* MESSAGE_H_ */
