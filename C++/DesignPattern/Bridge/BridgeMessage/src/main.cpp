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
	AbstractMessage* m = new CommonMessage();
	m->sendMessage("Tea", "Lee");

	m = new UrgencyMessage();
	m->sendMessage("Tea", "Lee");

	m = new SpecialUrgencyMessage();
	m->sendMessage("Tea", "Lee");

	std::cout << "\nTesting Mobile" << std::endl;
	m = new UrgencyMessage();
	m->sendMessage("Milk Tea", "Lee");

	m = new SpecialUrgencyMessage();
	m->sendMessage("Milk Tea", "Lee");

	std::cout << "\nTesting E-mail" << std::endl;
	m = new UrgencyMessage();
	m->sendMessage("Black Tea", "Lee");

	m = new SpecialUrgencyMessage();
	m->sendMessage("Black Tea", "Lee");
	return 0;
}
