/*
 * CPU.cpp
 *
 *  Created on: Oct 22, 2016
 *      Author: eliwech
 */

#include "CPU.h"

/* CPU */
CPU::CPU(Mediator* mediator)
	:Colleague(mediator)
{
}

CPU::~CPU()
{
}

std::string CPU::getSoundData() const
{
    return _soundData;
}
std::string CPU::getVideoData() const
{
    return _videoData;
}

void CPU::executeData(std::string video, std::string sound)
{
	/*6. put data into cpu */
	_videoData = video;
	_soundData = sound;
	/*7. inform mediator for next step*/
	getMediator()->changed(this);
}
