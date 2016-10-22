/*
 * VideoCard.h
 *
 *  Created on: Oct 22, 2016
 *      Author: eliwech
 */

#ifndef VIDEOCARD_H_
#define VIDEOCARD_H_

#include "Colleague.h"

class VideoCard : public Colleague
{
public:
	VideoCard(Mediator *mediator);
	virtual ~VideoCard();
	void showData(std::string data);
};

#endif /* VIDEOCARD_H_ */
