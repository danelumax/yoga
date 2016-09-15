/*
 * Transaction.h
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#ifndef TRANSACTION_H_
#define TRANSACTION_H_

class Transaction
{
public:
	Transaction(){};
	virtual ~Transaction(){};
	virtual int start() = 0;
	virtual int commit() = 0;

};

#endif /* TRANSACTION_H_ */
