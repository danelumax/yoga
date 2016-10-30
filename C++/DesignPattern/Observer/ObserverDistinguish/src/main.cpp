//============================================================================
// Name        : ObserverDistinguish.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "Watcher.h"
#include "WaterQuality.h"
#include "WatcherObserver.h"
#include "WaterQualitySubject.h"


int main()
{
	WaterQualitySubject* subject = new WaterQuality();

	WatcherObserver* watcher1 = new Watcher();
	watcher1->setJob("Surveillance Staff");
	WatcherObserver* watcher2 = new Watcher();
	watcher2->setJob("Alert Staff");
	WatcherObserver* watcher3 = new Watcher();
	watcher3->setJob("Surveillance Department Leader");

	subject->attach(watcher1);
	subject->attach(watcher2);
	subject->attach(watcher3);

	std::cout << "\nWhen Water Quality is Normal ---------->" << std::endl;
	subject->setPolluteLevel(0);
	std::cout << "\nWhen Water Quality is lightly polluted ---------->" << std::endl;
	subject->setPolluteLevel(1);
	std::cout << "\nWhen Water Quality is moderately polluted ---------->" << std::endl;
	subject->setPolluteLevel(2);
}
