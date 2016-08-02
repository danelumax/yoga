/*
 * LIWorksServer.h
 *
 *  Created on: 2016年1月31日
 *      Author: root
 */

#ifndef LIWORKSSERVER_H_
#define LIWORKSSERVER_H_

#include <iostream>
#include <string>
#include "EPCWorker.h"
#include "MessageQ.h"
#include "TcpServerSocket.h"
#include "XMLParse.h"
#include "WorkEngine.h"
#include <WorkEngineManager.h>

#define LOCALHOST "127.0.0.1"
#define POOLNUM 5

class LIWorksServer
{
public:
	virtual ~LIWorksServer();
	int init();
	int run();
	static void destory();
	static LIWorksServer* getInstance();
	int setupTcpServer(const char* addr, int port);
	int initWorkEngine();
	void destroyWorkEngine();
	void cleanUpResources();

protected:
	LIWorksServer();

private:
	static LIWorksServer *_instance;
	TcpServerSocket* _tcp_server;
    MessageQ *_msgQ;
};

#endif /* LIWORKSSERVER_H_ */
