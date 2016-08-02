/*
 * TcpServerSocket.h
 *
 *  Created on: 2016年2月1日
 *      Author: root
 */

#ifndef VERNAL_SERVER_SRC_TCPSERVERSOCKET_H_
#define VERNAL_SERVER_SRC_TCPSERVERSOCKET_H_

#include <TcpSocket.h>

class TcpServerSocket: public TcpSocket
{
public:
	TcpServerSocket(bool blocking=true);
	virtual ~TcpServerSocket();
	int listen(int queueLen=5);
	TcpSocket* accept();
};

#endif /* VERNAL_SERVER_SRC_TCPSERVERSOCKET_H_ */
