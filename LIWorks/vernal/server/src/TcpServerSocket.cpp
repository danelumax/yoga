/*
 * TcpServerSocket.cpp
 *
 *  Created on: 2016年2月1日
 *      Author: root
 */

#include "TcpServerSocket.h"

TcpServerSocket::TcpServerSocket(bool blocking):TcpSocket(blocking)
{
	// TODO Auto-generated constructor stub

}

TcpServerSocket::~TcpServerSocket()
{
	// TODO Auto-generated destructor stub
}

int TcpServerSocket::listen(int queueLen)
{
	int ret;

	ret = ::listen(_socket_fd, queueLen);
	if(ret < 0)
	{
		std::cout << "TcpServerSocket: Set listening socket failed !" << std::endl;
	}

	return ret;
}

TcpSocket* TcpServerSocket::accept()
{
	int newSocketFd;
	struct sockaddr *cliaddr=NULL;
	socklen_t *addrlen=0;

	newSocketFd = ::accept(_socket_fd, cliaddr, addrlen);
	if(newSocketFd < 0)
	{
		std::cout << "TcpServerSocket: Accept failed !" << std::endl;
		return NULL;
	}

	return new TcpSocket(newSocketFd);
}
