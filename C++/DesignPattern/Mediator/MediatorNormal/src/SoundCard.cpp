/*
 * SoundCard.cpp
 *
 *  Created on: Oct 22, 2016
 *      Author: eliwech
 */

#include "SoundCard.h"

/* SoundCard */
SoundCard::SoundCard(Mediator *mediator)
	:Colleague(mediator)
{
}

SoundCard::~SoundCard()
{
}

void SoundCard::soundData(std::string data)
{
	std::cout << "Listen: " << data << std::endl;
}
