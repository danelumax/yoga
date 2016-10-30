/*
 * WaterQualitySubject.h
 *
 *  Created on: Oct 30, 2016
 *      Author: eliwech
 */

#ifndef WATERQUALITYSUBJECT_H_
#define WATERQUALITYSUBJECT_H_

#include <vector>
#include "WatcherObserver.h"

class WaterQualitySubject
{
public:
	WaterQualitySubject();
	virtual ~WaterQualitySubject();
	void attach(WatcherObserver* observer);
	void detach(WatcherObserver* observer);
	virtual void notifyWatchers() = 0;
	virtual void setPolluteLevel(int polluteLevel) = 0;
	virtual int getPolluteLevel() = 0;
protected	:
	std::vector<WatcherObserver*> _observers;
};

#endif /* WATERQUALITYSUBJECT_H_ */
