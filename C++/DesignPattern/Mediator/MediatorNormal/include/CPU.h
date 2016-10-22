/*
 * CPU.h
 *
 *  Created on: Oct 22, 2016
 *      Author: eliwech
 */

#ifndef CPU_H_
#define CPU_H_

#include "Colleague.h"

class CPU : public Colleague
{
public:
	CPU(Mediator *mediator);
	virtual ~CPU();
    std::string getSoundData() const;
    std::string getVideoData() const;

    void executeData(std::string video, std::string sound);
private:
	std::string _videoData;
	std::string _soundData;
};

#endif /* CPU_H_ */
