//============================================================================
// Name        : TemplateClass.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <iostream>
#include <string>
#include "MessageQ.h"

int main()
{
	MessageQ<int> *msgQint = new MessageQ<int>();
	MessageQ<std::string> *msgQstring = new MessageQ<std::string>();

	int tmpInt = msgQint->MerageMessage(1, 2);
	std::string tmpString = msgQstring->MerageMessage("hello", "world");
	std::cout << "Int: " << tmpInt <<"\nString: " << tmpString << std::endl;
	return 0;
}
