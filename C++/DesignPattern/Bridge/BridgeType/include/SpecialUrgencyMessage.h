/*
 * SpecialUrgencyMessage.h
 *
 *  Created on: Oct 2, 2016
 *      Author: eliwech
 */

#ifndef SPECIALURGENCYMESSAGE_H_
#define SPECIALURGENCYMESSAGE_H_

#include "AbstractMessage.h"
//#include "MessageImplementor.h"

class SpecialUrgencyMessage : public AbstractMessage
{
public:
	SpecialUrgencyMessage(AbstractMessage::MessageType type);
	virtual ~SpecialUrgencyMessage();
	virtual void sendMessage(std::string message, std::string toUser);
};

#endif /* SPECIALURGENCYMESSAGE_H_ */
