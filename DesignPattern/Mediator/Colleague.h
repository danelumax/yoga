/*
 * Colleague.h
 *
 *  Created on: Aug 8, 2016
 *      Author: eliwech
 */

#ifndef COLLEAGUE_H_
#define COLLEAGUE_H_

#include <string>
#include <iostream>
class Mediator;

/***** Declaration *****/
class Colleague
{
public:
	//wait derived class to call, tell colleague, you need to inform who
	Colleague(Mediator *mediator);
	virtual ~Colleague(){};
	Mediator* getMediator()
	{
		return _mediator;
	}
private:
	Mediator *_mediator;
};

class CDDriver : public Colleague
{
public:
	CDDriver(Mediator *mediator);
	virtual ~CDDriver(){};
	std::string getData()
	{
		return _data;
	}
	void readCD();
private:
	std::string _data;
};

class CPU : public Colleague
{
public:
	CPU(Mediator *mediator);
	virtual ~CPU(){};
    std::string getSoundData() const
    {
        return _soundData;
    }
    std::string getVideoData() const
    {
        return _videoData;
    }
    void executeData(std::string video, std::string sound);
private:
	std::string _videoData;
	std::string _soundData;
};

class VideoCard : public Colleague
{
public:
	VideoCard(Mediator *mediator);
	virtual ~VideoCard(){};
	void showData(std::string data);
};

class SoundCard : public Colleague
{
public:
	SoundCard(Mediator *mediator);
	virtual ~SoundCard(){};
	void soundData(std::string data);
};




#endif /* COLLEAGUE_H_ */
