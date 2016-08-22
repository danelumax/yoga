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

int main()
{
	int listenfd, connfd;
	int nready;
	ssize_t n;
	char buf[MAXLINE];
	socklen_t clilen;
	struct pollfd client;
	struct sockaddr_in cliaddr, servaddr;

	listenfd = ::socket(AF_INET, SOCK_STREAM, 0);

	bzero(&servaddr, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = htonl(INADDR_ANY);
	servaddr.sin_port = htons(SERV_PORT);

	::bind(listenfd, (struct sockaddr*)&servaddr, sizeof(servaddr));

	::listen(listenfd, 1024);

	client.fd = listenfd;
	client.events = POLLIN;

	while(1)
	{
		nready = ::poll(&client, 1, -1); // -1:infinite

		if(client.revents & POLLIN)
		{
 			clilen = sizeof(cliaddr);
			connfd = ::accept(listenfd, (struct sockaddr*)&cliaddr, &clilen);

			n = ::recv(connfd, buf, MAXLINE, 0);
			if (n > 0)
			{
				std::string message(buf);
				std::cout << "Receive message: " << message << std::endl;
			}
		}
	}
}
