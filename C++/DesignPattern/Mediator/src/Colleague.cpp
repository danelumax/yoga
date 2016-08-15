/*
 * Colleague.cpp
 *
 *  Created on: Aug 10, 2016
 *      Author: eliwech
 */

#include "Colleague.h"
#include "Mediator.h"

/***** Definition*****/
/* Colleague */
Colleague::Colleague(Mediator *mediator)
{
	_mediator = mediator;
}

/* CDDriver */
CDDriver::CDDriver(Mediator *mediator)
	:Colleague(mediator)
{
}

void CDDriver::readCD()
{
	/*1. Mock store data from CD */
	_data = "Movie";
	/*2. inform mediator for next step*/
	getMediator()->changed(this);
}

/* CPU */
CPU::CPU(Mediator* mediator)
	:Colleague(mediator)
{
}

void CPU::executeData(std::string video, std::string sound)
{
	/*6. put data into cpu */
	_videoData = video;
	_soundData = sound;
	/*7. inform mediator for next step*/
	getMediator()->changed(this);
}

/* VideoCard */
VideoCard::VideoCard(Mediator *mediator)
	:Colleague(mediator)
{
}

void VideoCard::showData(std::string data)
{
	std::cout << "Watch: " << data << std::endl;
}

/* SoundCard */
SoundCard::SoundCard(Mediator *mediator)
	:Colleague(mediator)
{
}

void SoundCard::soundData(std::string data)
{
	std::cout << "Listen: " << data << std::endl;
}
