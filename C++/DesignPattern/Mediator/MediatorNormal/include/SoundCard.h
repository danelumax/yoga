/*
 * SoundCard.h
 *
 *  Created on: Oct 22, 2016
 *      Author: eliwech
 */

#ifndef SOUNDCARD_H_
#define SOUNDCARD_H_

#include "Colleague.h"

class SoundCard : public Colleague
{
public:
	SoundCard(Mediator *mediator);
	virtual ~SoundCard();
	void soundData(std::string data);
};

#endif /* SOUNDCARD_H_ */
