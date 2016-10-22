/*
 * MotherBoard.cpp
 *
 *  Created on: Aug 8, 2016
 *      Author: eliwech
 */

#include "MotherBoard.h"

MotherBoard::MotherBoard()
{
}

MotherBoard::~MotherBoard()
{
}

void MotherBoard::setCdDriver(CDDriver *cdDriver)
{
    _cdDriver = cdDriver;
}

void MotherBoard::setCpu(CPU *cpu)
{
    _cpu = cpu;
}

void MotherBoard::setSoundCard(SoundCard *soundCard)
{
    _soundCard = soundCard;
}

void MotherBoard::setVideoCard(VideoCard *videoCard)
{
    _videoCard = videoCard;
}

void MotherBoard::openCDDriverReadData(CDDriver *cd)
{
	/*4. read data from CDDriver */
	std::string data = cd->getData();
	/*5. put videoData, SoundData into cpu*/
	_cpu->executeData(data, "love song");
}

void MotherBoard::openCPU(CPU *cpu)
{
	/*9. get data from CPU */
	std::string videoData = cpu->getVideoData();
	std::string soundData = cpu->getSoundData();

	/*10. Mediator to show data */
	_videoCard->showData(videoData);
	_soundCard->soundData(soundData);
}

void MotherBoard::changed(Colleague *colleague)
{
	if (colleague == _cdDriver)
	{
		/*3. Mediator inform cpu to get data */
		openCDDriverReadData(dynamic_cast<CDDriver*>(colleague));
	}
	else if (colleague == _cpu)
	{
		/*8. Mediator will show data */
		openCPU(dynamic_cast<CPU*>(colleague));
	}
}




