//============================================================================
// Name        : ContextFSM.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <vector>
#include <iostream>
#include <boost/assign.hpp>
#include <Message.h>
#include <DiaSessionContext.h>
#include <MessageFactory.h>

std::vector<std::string> AuthenTraffic = boost::assign::list_of
	("DER")("MAA")("SAA")("DER")("SAA");

std::vector<std::string> AuthorTraffic = boost::assign::list_of
	("AAR")("SAA");

int main()
{
	Message *msg = NULL;
	DiaSessionContext* context = new DiaSessionContext();
	std::string splitLine = "\n\n*********************\n";

	std::cout <<  splitLine << "Start Authentication ..." << std::endl;
	std::vector<std::string>::iterator iter = AuthenTraffic.begin();
	for(; iter!=AuthenTraffic.end(); ++iter)
	{
		msg = MessageFactory::getInstance()->getMessage(*iter);
		context->process(msg);
	}

	context = new DiaSessionContext();
	std::cout << splitLine << "Start Authorization ..." << std::endl;
	iter = AuthorTraffic.begin();
	for(; iter!=AuthorTraffic.end(); ++iter)
	{
		msg = MessageFactory::getInstance()->getMessage(*iter);
		context->process(msg);
	}

	return 0;
}
