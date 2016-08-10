//============================================================================
// Name        : Mediator.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "Colleague.h"
#include "MotherBoard.h"

int main()
{
	MotherBoard *mediator = new MotherBoard();

	CDDriver *cd = new CDDriver(mediator);
	CPU *cpu = new CPU(mediator);
	VideoCard *vc = new VideoCard(mediator);
	SoundCard *sc = new SoundCard(mediator);

	mediator->setCdDriver(cd);
	mediator->setCpu(cpu);
	mediator->setVideoCard(vc);
	mediator->setSoundCard(sc);

	cd->readCD();
}
