/*
 * WaterQuality.h
 *
 *  Created on: Oct 30, 2016
 *      Author: eliwech
 */

#ifndef WATERQUALITY_H_
#define WATERQUALITY_H_

#include "WaterQualitySubject.h"

class WaterQuality : public WaterQualitySubject
{
public:
	WaterQuality();
	virtual ~WaterQuality();
	virtual void setPolluteLevel(int polluteLevel);
	virtual void notifyWatchers();
	virtual int getPolluteLevel();
private:
	int _polluteLevel;
};

#endif /* WATERQUALITY_H_ */
