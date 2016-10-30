/*
 * WaterQuality.cpp
 *
 *  Created on: Oct 30, 2016
 *      Author: eliwech
 */

#include "WaterQuality.h"

WaterQuality::WaterQuality()
	:_polluteLevel(0)
{
}

WaterQuality::~WaterQuality()
{
}

void WaterQuality::setPolluteLevel(int polluteLevel)
{
	_polluteLevel = polluteLevel;
	notifyWatchers();
}

void WaterQuality::notifyWatchers()
{
	std::vector<WatcherObserver*>::iterator iter = _observers.begin();
	for(; iter!=_observers.end(); ++iter)
	{
		if (_polluteLevel >= 0)
		{
			if ("Surveillance Staff" == (*iter)->getJob())
			{
				(*iter)->update(this);
			}
		}

		if (_polluteLevel >= 1)
		{
			if ("Alert Staff" == (*iter)->getJob())
			{
				(*iter)->update(this);
			}
		}

		if (_polluteLevel >= 2)
		{
			if ("Surveillance Department Leader" == (*iter)->getJob())
			{
				(*iter)->update(this);
			}
		}
	}
}

int WaterQuality::getPolluteLevel()
{
	return _polluteLevel;
}
