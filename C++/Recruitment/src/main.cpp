#include "AddressServer.h"

int main()
{
	AddressServer* server = AddressServer::getInstance();
	server->init();
	server->run();

    return 0;
}
