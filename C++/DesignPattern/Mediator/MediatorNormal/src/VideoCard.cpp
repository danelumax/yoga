/*
 * VideoCard.cpp
 *
 *  Created on: Oct 22, 2016
 *      Author: eliwech
 */

#include "VideoCard.h"

/* VideoCard */
VideoCard::VideoCard(Mediator *mediator)
	:Colleague(mediator)
{
}

VideoCard::~VideoCard()
{
}

void VideoCard::showData(std::string data)
{
	std::cout << "Watch: " << data << std::endl;
}
