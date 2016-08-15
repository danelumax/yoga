/*
 * Socket.cpp
 *
 *  Created on: 2016年2月1日
 *      Author: root
 */

#include "Socket.h"

Socket::Socket(int socket_fd)
{
	_socket_fd = socket_fd;
}

Socket::Socket(int type, int protocol, bool blocking)
{
	_socket_fd = -1;
	const int optval = 1;

	_socket_fd = socket(AF_INET, type, protocol);
	if(_socket_fd < 0)
	{
		std::cout << "Socket creation failed!" << std::endl;
	}

	if(!blocking)
	{
		int flag;

		flag = fcntl(_socket_fd, F_GETFL, 0);
		if(-1 == flag)
		{
			std::cout << "Serious error using fcntl" << std::endl;
		}
		else
		{
			flag |= O_NONBLOCK;
			fcntl(_socket_fd, F_SETOWN, getpid());
			if(fcntl(_socket_fd, F_SETFL, flag) != 0)
			{
				std::cout << "Setting of blocking flag failed!" << std::endl;
			}
		}
	}
	if (setsockopt(_socket_fd, SOL_SOCKET, SO_REUSEADDR,&optval, sizeof(optval)) != 0)
	{
		std::cout << "setsockopt failed!" << std::endl;
	}
}

Socket::~Socket() {
	// TODO Auto-generated destructor stub
}

void Socket::fillAddr(const char* address, unsigned short port, struct sockaddr_in &addr)
{
	memset(&addr, 0, sizeof(addr));
	addr.sin_family = AF_INET;

	if(address && address[0])
	{
		struct hostent host, *phost;
		char buffer[256];
		int err_no;

		if(gethostbyname_r(address, &host, buffer, sizeof(buffer), &phost, &err_no) == 0)
		{
			struct addrinfo *answer = NULL;
			struct addrinfo hint;
			bzero(&hint, sizeof(hint));
			hint.ai_family = AF_INET;
			int ret = getaddrinfo(address, NULL, &hint, &answer);
			if(0 == ret)
			{
				if(NULL != answer)
				{
					addr.sin_addr = ((struct sockaddr_in *)(answer->ai_addr))->sin_addr;
					freeaddrinfo(answer);
				}
			}
		}
		else
		{
			addr.sin_addr = *((in_addr *)host.h_addr_list[0]);
		}
	}
	else
	{
		addr.sin_addr.s_addr = htonl(INADDR_ANY);
	}
	addr.sin_port = htons(port);

}

int Socket::bind(const char* localAddress, unsigned short localPort)
{
	struct sockaddr_in localAddr;
	fillAddr(localAddress, localPort, localAddr);

	int ret;
	ret = ::bind(_socket_fd, (struct sockaddr *)&localAddr, sizeof(struct sockaddr_in));
	if(ret < 0)
	{
		std::cout << "Bind local address and port failed!" <<std::endl;
	}

	return ret;
}

