/*
 * Watcher.cpp
 *
 *  Created on: Oct 30, 2016
 *      Author: eliwech
 */

#include "Watcher.h"

Watcher::Watcher()
	:_job("")
{
}

Watcher::~Watcher()
{
}

void Watcher::update(WaterQualitySubject* subject)
{
	std::cout << "<" << _job << "> get the notification, current pollute level: "
			  << subject->getPolluteLevel() << std::endl;
}

void Watcher::setJob(std::string job)
{
	_job = job;
}

std::string Watcher::getJob()
{
	return _job;
}
