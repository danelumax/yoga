/*
 * LIWorksServer.cpp
 *
 *  Created on: 2016年1月31日
 *      Author: root
 */

#include "LIWorksServer.h"

LIWorksServer* LIWorksServer::_instance=NULL;

LIWorksServer::LIWorksServer()
{
	_tcp_server = new TcpServerSocket();
	_msgQ = NULL;
}

LIWorksServer::~LIWorksServer()
{
	delete _tcp_server;
	_tcp_server = NULL;
	delete _msgQ;
	_msgQ = NULL;
}

LIWorksServer* LIWorksServer::getInstance()
{
	if(_instance == NULL)
	{
		_instance = new LIWorksServer();
	}

	return _instance;
}

void LIWorksServer::destory()
{
	if(_instance != NULL)
	{
		_instance->cleanUpResources();

		delete _instance;
		_instance = NULL;
	}
}

int LIWorksServer::setupTcpServer(const char* addr, int port)
{
	int ret;
	if(addr == NULL)
		return -1;

	ret = _tcp_server->bind(addr, port);
	if(ret < 0)
	{
		std::cout << "bind failed" << std::endl;
		return ret;
	}

	ret = _tcp_server->listen();
	if(ret < 0)
	{
		std::cout << "Core Server: listen on the socket failed!" << std::endl;
		return ret;
	}

	return 0;
}

int LIWorksServer::initWorkEngine()
{
	int type = 1;
	WorkEngine* engine = new WorkEngine(POOLNUM);
	engine->initWorkerList();
	if(WorkEngineManager::getInstance()->registerWorkEngine(1, engine) !=0)
	{
		delete engine;
		return -1;
	}

	return 0;

}

int LIWorksServer::init()
{
	int ret;
	const char* localAddr = LOCALHOST;
	int port = 8899;

	std::cout << "LIWorksServer starting ..." << std::endl;

	//创建一个全局的messageQ
	StringMessageQ::getInstance()->initMessageQueue();
	_msgQ = StringMessageQ::getInstance()->getmsgQ();

	if(initWorkEngine() != 0)
	{
		std::cout << "WorkEnging init failed" << std::endl;
		return -1;
	}

	//parse xml
	XMLParse *xml = new XMLParse();
	xml->ParseXMLFile();

	ret = setupTcpServer(localAddr, port);
	if(ret < 0)
	{
		std::cout << "CoreServer listen failed" << std::endl;
		return -1;
	}

	delete xml;

	return 0;
}

int LIWorksServer::run()
{
	int ret;
	char buffer[1024];

	WorkEngineManager::getInstance()->startAllWorkEngines();

	TcpSocket *socket;
	while(1)
	{
		socket = _tcp_server->accept();
		if(NULL == socket)
		{
			std::cout << "CoreServer accept failed" << std::endl;
			return 1;
		}

		memset(buffer, 0, sizeof(buffer));
		ret = socket->recv(buffer, 1024);
		if(ret < 0)
		{
			delete socket;
			std::cout << "receive message failed" << std::endl;
			return ret;
		}

		std::string message = buffer;
		if("quit" != message)
		{
			_msgQ->try_put(message);
		}
		else
		{
			std::cout << "connection cancel" << std::endl;
			break;
		}
	}

	delete socket;
	socket = NULL;

	return 0;
}

void LIWorksServer::destroyWorkEngine()
{
	WorkEngineManager::getInstance()->clearWorkEngines();
	std::cout << "LIWorksServer:: destroy engine successfully." << std::endl;
}

void LIWorksServer::cleanUpResources()
{
	destroyWorkEngine();
}
