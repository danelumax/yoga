/*
 * WaterQualitySubject.cpp
 *
 *  Created on: Oct 30, 2016
 *      Author: eliwech
 */

#include "WaterQualitySubject.h"

WaterQualitySubject::WaterQualitySubject()
{
}

WaterQualitySubject::~WaterQualitySubject()
{
}

void WaterQualitySubject::attach(WatcherObserver* observer)
{
	_observers.push_back(observer);
}

void WaterQualitySubject::detach(WatcherObserver* observer)
{
	std::vector<WatcherObserver*>::iterator iter = _observers.begin();
	for(; iter!=_observers.end(); ++iter)
	{
		if ((*iter) == observer)
		{
			delete (*iter);
			_observers.erase(iter);
			iter = _observers.begin();
		}
	}
}
