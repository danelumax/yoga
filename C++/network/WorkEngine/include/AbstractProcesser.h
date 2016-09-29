/*
 * AbstractProcesser.h
 *
 *  Created on: Sep 29, 2016
 *      Author: eliwech
 */

#ifndef ABSTRACTPROCESSER_H_
#define ABSTRACTPROCESSER_H_

#include <string>

class AbstractProcesser
{
public:
	virtual ~AbstractProcesser();
	static AbstractProcesser* getInstance();
	void processMessage();
private:
	AbstractProcesser();
	static AbstractProcesser* _instance;
};

#endif /* ABSTRACTPROCESSER_H_ */
