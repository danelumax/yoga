//============================================================================
// Name        : PollMutiConnection.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <sys/types.h>  //ssize_t
#include <sys/socket.h> //socket, AF_INET, listen
#include <sys/poll.h>   //pollfd, POLLIN
#include <netinet/in.h> //sockaddr_in
#include <string.h>     //bzero
#include <string>
#include <iostream>

const int MAXLINE = 4096;
const int SERV_PORT = 9877;
const int OPEN_MAX = 10;

int main()
{
	int i, maxi, listenfd, connfd, sockfd;
	int nready;
	ssize_t n;
	char buf[MAXLINE];
	socklen_t clilen;
	struct pollfd client[OPEN_MAX];
	struct sockaddr_in cliaddr, servaddr;

	listenfd = ::socket(AF_INET, SOCK_STREAM, 0);

	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	servaddr.sin_port = htons(SERV_PORT);

	::bind(listenfd, (struct sockaddr*)&servaddr, sizeof(servaddr));

	::listen(listenfd, 1024);

	client[0].fd = listenfd;
	client[0].events = POLLIN;
	for(i=1; i<OPEN_MAX; i++)
	{
		client[i].fd = -1;
	}
	maxi = 0;

	while(1)
	{
		nready = ::poll(client, maxi+1, -1); // -1:infinite

		if(client[0].revents & POLLIN)
		{
 			clilen = sizeof(cliaddr);
			connfd = ::accept(listenfd, (struct sockaddr*)&cliaddr, &clilen);

			for(i=1; i<OPEN_MAX; i++)
			{
				if (client[i].fd < 0)
				{
					client[i].fd = connfd;
					std::cout << "Now we have established " << i << " connections" << std::endl;
					break;
				}
			}

			client[i].events = POLLIN;
			if(i > maxi)
			{
				maxi = i;
			}

			if(--nready <= 0)
			{
				continue;
			}
		}

		for(int i=1; i<=maxi; i++)
		{
			sockfd = client[i].fd;
			if (sockfd < 0)
			{
				continue;
			}

			if (client[i].revents & POLLIN)
			{
				n = ::recv(sockfd, buf, MAXLINE, 0);
				if (n > 0)
				{
					std::string message(buf);
					std::cout << "Receive message: " << message << std::endl;
				}
				else if(n == 0)
				{
					std::cout << "Remote client close." << std::endl;
					close(sockfd);
					client[i].fd = -1;
				}

				if (--nready <= 0)
				{
					break;
				}
			}
		}
	}
}
