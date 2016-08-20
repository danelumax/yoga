//============================================================================
// Name        : Select.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================


#include <sys/select.h> //FD_SETSIZE, fd_set
#include <sys/types.h>  //ssize_t
#include <sys/socket.h> //socket, AF_INET, SOCK_STREAM, listen
#include <netinet/in.h> //sockaddr_in
#include <string.h>		//bzero
#include <iostream>
#include <string>

const int MAXLINE = 4096;
const int SERV_PORT = 9877;

int main()
{
	int maxfd, listenfd, connfd;
	int nready;
	fd_set rset;
	char buf[MAXLINE];
	socklen_t clilen;
	struct sockaddr_in cliaddr, servaddr;

	listenfd = ::socket(AF_INET, SOCK_STREAM, 0);

	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	servaddr.sin_port = htons(SERV_PORT);

	::bind(listenfd, (struct sockaddr*)&servaddr, sizeof(servaddr));

	::listen(listenfd, 1024);

	while(1)
	{
		/* reload fd_set */
		FD_ZERO(&rset);
		FD_SET(listenfd, &rset);
		maxfd = listenfd;

		/* Focus on listenfd, wait for listenfd state changing */
		nready = ::select(maxfd+1, &rset, NULL, NULL, NULL);
		if (nready < 0)
		{
			std::cout << "select error" <<std::endl;
			continue;
		}
		else
		{
			std::cout << " * listenfd state changing * " <<std::endl;
		}
		if (FD_ISSET(listenfd, &rset))
		{
			std::cout << "Now we have established " << nready << " connections" <<std::endl;
			clilen = sizeof(cliaddr);
			if ((connfd = ::accept(listenfd, (struct sockaddr*)&cliaddr, &clilen)) < 0)
			{
				std::cout << "accept error" <<std::endl;
				return -1;
			}

			ssize_t n = ::recv(connfd, buf, MAXLINE, 0);
			if (n > 0)
			{
				std::string message(buf);
				std::cout << "Receive message: "<< message << std::endl;
			}

		}
	}
	return 0;
}
