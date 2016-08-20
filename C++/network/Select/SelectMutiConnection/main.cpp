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
#include <stdio.h>
#include <string>

const int MAXLINE = 4096;
const int SERV_PORT = 9877;


int main()
{
	int i, maxi, maxfd, listenfd, connfd, sockfd;
	int nready, client[FD_SETSIZE];
	ssize_t n;
	fd_set rset, allset;
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

	maxfd = listenfd;
	maxi = -1;
	for(i=0; i<FD_SETSIZE; i++)
	{
		client[i] = -1;
	}
	FD_ZERO(&allset);
	FD_SET(listenfd, &allset);

	while(1)
	{
		/* reload new fd_set, last time one connection was established */
		rset = allset;
		/* Focus on listenfd, wait for listenfd state changing */
		nready = ::select(maxfd+1, &rset, NULL, NULL, NULL);

		if (FD_ISSET(listenfd, &rset))
		{
			std::cout << "Now we have established " << nready << " connections" <<std::endl;
			clilen = sizeof(cliaddr);
			connfd = ::accept(listenfd, (struct sockaddr*)&cliaddr, &clilen);

			for(i=0; i<FD_SETSIZE; i++)
			{
				/* if client i-th slot has not be used */
				if (client[i] < 0)
				{
					/* add one connection */
					client[i] = connfd;
					break;
				}
			}

			/* One slot will be added into fd_set in every time connection */
			FD_SET(connfd, &allset);
			/* update max connection number */
			if (connfd > maxfd)
			{
				maxfd = connfd;
			}
			if (i > maxi)
			{
				maxi = i;
			}
			/* first start, accept has not be resigster into fd_set
			 * so skipp fisrt time, so nready = 1(just listen) can be ignore,
			 * then the second time, nready=2(listen + accept) can pass
			 */
			if (--nready <= 0)
			{
				continue;
			}
		}

		for(int i=0; i<=maxi; i++)
		{
			sockfd = client[i];
			if (sockfd < 0)
			{
				continue;
			}

			if (FD_ISSET(sockfd, &rset))
			{
				n = ::read(sockfd, buf, MAXLINE);
				if (n > 0)
				{
					std::string message(buf);
					std::cout << "Receive message: "<< message << std::endl;
				}
			}
			else
			{
				close(sockfd);
				FD_CLR(sockfd, &allset);
				client[i] = -1;
				std::cout << "error" << std::endl;
			}

			/* when just remain listenfd, break, otherwise it will check sockfd(connfd) */
			if (--nready <= 0)
			{
				break;
			}
		}
	}
	return 0;
}
