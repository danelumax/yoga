/*
 * Socket.h
 *
 *  Created on: 2016年2月1日
 *      Author: root
 */

#ifndef VERNAL_SERVER_SRC_SOCKET_H_
#define VERNAL_SERVER_SRC_SOCKET_H_

#include <sys/socket.h>
#include <iostream>
#include <string.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include <fcntl.h>

class Socket
{
public:
	virtual ~Socket();
	int bind(const char* localAddress, unsigned short localPort);
	static void fillAddr(const char* address, unsigned short port, struct sockaddr_in &addr);
protected:
	Socket(int socket_fd);
	Socket(int type, int protocol, bool blocking = true);
	int _socket_fd;
};

#endif /* VERNAL_SERVER_SRC_SOCKET_H_ */
