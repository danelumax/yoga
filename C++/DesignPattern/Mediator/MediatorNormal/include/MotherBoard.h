/*
 * MotherBoard.h
 *
 *  Created on: Aug 8, 2016
 *      Author: eliwech
 */

#ifndef MOTHERBOARD_H_
#define MOTHERBOARD_H_

#include "Mediator.h"
#include "CDDriver.h"
#include "CPU.h"
#include "SoundCard.h"
#include "VideoCard.h"

class MotherBoard : public Mediator
{
public:
	MotherBoard();
	virtual ~MotherBoard();
	virtual void changed(Colleague *colleague);

    void setCdDriver(CDDriver *cdDriver);
    void setCpu(CPU *cpu);
    void setSoundCard(SoundCard *soundCard);
    void setVideoCard(VideoCard *videoCard);
    void openCDDriverReadData(CDDriver *cd);
    void openCPU(CPU *cpu);

private:
	CDDriver *_cdDriver;
	CPU *_cpu;
	VideoCard *_videoCard;
	SoundCard *_soundCard;
};

#endif /* MOTHERBOARD_H_ */
