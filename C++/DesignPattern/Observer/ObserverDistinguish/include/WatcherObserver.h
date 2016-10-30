/*
 * WatcherObserver.h
 *
 *  Created on: Oct 30, 2016
 *      Author: eliwech
 */

#ifndef WATCHEROBSERVER_H_
#define WATCHEROBSERVER_H_

#include <string>

class WaterQualitySubject;

class WatcherObserver
{
public:
	virtual void update(WaterQualitySubject* subject) = 0;
	virtual void setJob(std::string job) = 0;
	virtual std::string getJob() = 0;
};

#endif /* WATCHEROBSERVER_H_ */
