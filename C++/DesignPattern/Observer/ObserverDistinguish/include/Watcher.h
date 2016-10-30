/*
 * Watcher.h
 *
 *  Created on: Oct 30, 2016
 *      Author: eliwech
 */

#ifndef WATCHER_H_
#define WATCHER_H_

#include <iostream>
#include "WatcherObserver.h"
#include "WaterQualitySubject.h"

class Watcher : public WatcherObserver
{
public:
	Watcher();
	virtual ~Watcher();
	virtual void update(WaterQualitySubject* subject);
	virtual void setJob(std::string job);
	virtual std::string getJob();
private:
	std::string _job;
};

#endif /* WATCHER_H_ */
