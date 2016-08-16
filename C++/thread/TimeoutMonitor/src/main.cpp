//============================================================================
// Name        : TimeoutMonitor.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <iostream>
#include <TimeoutMonitor.h>

int main(void)
{
	TimeoutMonitor *monitor = TimeoutMonitor::getInstance();

	/* start monitor, print info in every interval */
	std::cout << "Start monitor ..." << std::endl;
	monitor->start();
	sleep(10);

	/* stop monitor */
	monitor->stop();
	std::cout << "Stop monitor successfully!" << std::endl;

	sleep(100);
	return 0;
}
