/*
 * TcpSocket.h
 *
 *  Created on: 2016年2月1日
 *      Author: root
 */

#ifndef VERNAL_SERVER_SRC_TCPSOCKET_H_
#define VERNAL_SERVER_SRC_TCPSOCKET_H_

#include "Socket.h"

class TcpSocket:public Socket
{
public:
	TcpSocket(int fd);
	TcpSocket(bool blocking=true);
	virtual ~TcpSocket();
	int recv(void* buffer, int len);
};

#endif /* VERNAL_SERVER_SRC_TCPSOCKET_H_ */
