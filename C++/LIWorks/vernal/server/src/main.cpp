//============================================================================
// Name        : LIWorks.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "LIWorksServer.h"

int main(void)
{
	int ret;
	LIWorksServer *server;

	server= LIWorksServer::getInstance();
	ret = server->init();
	ret = server->run();

	LIWorksServer::destory();

	return ret;
}
