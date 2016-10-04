//============================================================================
// Name        : BridgeExp1.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <iostream>
#include "CommonMessage.h"
#include "UrgencyMessage.h"
#include "AbstractMessage.h"
#include "SpecialUrgencyMessage.h"

int main(void)
{
	std::cout << "\nTesting SMS" << std::endl;
	AbstractMessage* m = new CommonMessage(AbstractMessage::SMS);
	m->sendMessage("Tea", "Lee");

	m = new UrgencyMessage(AbstractMessage::SMS);
	m->sendMessage("Tea", "Lee");

	m = new SpecialUrgencyMessage(AbstractMessage::SMS);
	m->sendMessage("Tea", "Lee");

	std::cout << "\nTesting Mobile" << std::endl;
	m = new CommonMessage(AbstractMessage::MOBILE);
	m->sendMessage("Tea", "Lee");

	m = new UrgencyMessage(AbstractMessage::MOBILE);
	m->sendMessage("Tea", "Lee");

	std::cout << "\nTesting E-mail" << std::endl;
	m = new SpecialUrgencyMessage(AbstractMessage::EMAIL);
	m->sendMessage("Tea", "Lee");
	return 0;
}
