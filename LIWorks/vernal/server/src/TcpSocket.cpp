/*
 * TcpSocket.cpp
 *
 *  Created on: 2016年2月1日
 *      Author: root
 */

#include "TcpSocket.h"

TcpSocket::TcpSocket(bool blocking):Socket(SOCK_STREAM, 0, blocking)
{
}

TcpSocket::TcpSocket(int fd):Socket(fd)
{
}

TcpSocket::~TcpSocket() {
	// TODO Auto-generated destructor stub
}

int TcpSocket::recv(void* buffer, int len)
{
	char *ptr = (char*)buffer;

	int dataReadCount = 0;
	int restToRead = len - dataReadCount;
	int currentReadCount = 0;

	currentReadCount = ::recv(_socket_fd, (ptr+dataReadCount), restToRead, 0);
	if(currentReadCount <= 0)
	{
		std::cout << "TcpSocket::recv failed!" << std::endl;
	}
	else
	{
		dataReadCount += currentReadCount;
		restToRead -= currentReadCount;
		if(restToRead > 0)
		{
			//std::cout << "TcpSocket::recv --> continue to receive the rest message length = " << restToRead << std::endl;
			std::cout << "\n> > > > > > > > > > > > > > > > > > > >" << std::endl;
			std::cout << "Receive message : " << (char*)buffer << std::endl;
		}
	}
	return dataReadCount;
}

