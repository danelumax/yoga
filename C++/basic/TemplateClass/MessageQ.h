/*
 * MessageQ.h
 *
 *  Created on: Aug 15, 2016
 *      Author: eliwech
 */

#ifndef MESSAGEQ_H_
#define MESSAGEQ_H_

#include <string>

template<typename QType>
class MessageQ
{
public:
	MessageQ(){};
	~MessageQ(){};
	QType MerageMessage(QType messageA, QType messageB);
};

/**
 * For Avoid template class function show undefined reference in compiling
 * Put template function definitions in its header file
 */

template<typename QType>
QType MessageQ<QType>::MerageMessage(QType messageA, QType messageB)
{
	QType tmp = messageA + messageB;
	return tmp;
}


#endif /* MESSAGEQ_H_ */
