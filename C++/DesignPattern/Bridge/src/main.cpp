//============================================================================
// Name        : BridgeExp1.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <iostream>
#include "MessageSMS.h"
#include "CommonMessage.h"
#include "MessageMobile.h"
#include "UrgencyMessage.h"
#include "AbstractMessage.h"
#include "MessageImplementor.h"
#include "SpecialUrgencyMessage.h"

int main(void)
{
	std::cout << "\nTesting SMS" << std::endl;
	MessageImplementor* impl = new MessageSMS;
	AbstractMessage* m = new CommonMessage(impl);
	m->sendMessage("Tea", "Lee");

	m = new UrgencyMessage(impl);
	m->sendMessage("Tea", "Lee");

	m = new SpecialUrgencyMessage(impl);
	m->sendMessage("Tea", "Lee");

	std::cout << "\nTesting Mobile" << std::endl;
	impl = new MessageMobile;
	m = new CommonMessage(impl);
	m->sendMessage("Tea", "Lee");

	m = new UrgencyMessage(impl);
	m->sendMessage("Tea", "Lee");

	m = new SpecialUrgencyMessage(impl);
	m->sendMessage("Tea", "Lee");
	return 0;
}
