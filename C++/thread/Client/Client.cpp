#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <string.h>
#include <string>
#include <netdb.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include "unistd.h"

#define SERV_PORT 9877
#define MAXBUFFER 1024

int main(int argc, char* argv[])
{
        char* message = argv[1];
        //std::string message = argv[1];
	int socket_fd;
	char buf[MAXBUFFER];
	struct sockaddr_in servaddr;
	int ret;

	if((socket_fd = socket(AF_INET, SOCK_STREAM, 0)) == -1)
	{
		perror("create socket error");
		exit(-1);
	}

	memset(&servaddr, 0, sizeof(servaddr));
	servaddr.sin_family = AF_INET;
	servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");
	servaddr.sin_port = htons(SERV_PORT);

	ret = connect(socket_fd, (struct sockaddr * )& servaddr, sizeof(servaddr));
	if(ret == -1)
	{
		perror("cannot connect  to the server");
		exit(-1);
	}
	write(socket_fd, message, strlen(message));

	close(socket_fd);

	return 0;
}
