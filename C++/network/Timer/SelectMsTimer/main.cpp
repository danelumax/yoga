//============================================================================
// Name        : SelectMsTimer.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <sys/select.h>
#include <time.h>
#include <iostream>

/* using select to count ms is more accurate than usleep */
static void SleepMs(int sleepTime)
{
	int ret;
	struct timeval tv;
	tv.tv_sec = sleepTime/1000;
	tv.tv_usec = (sleepTime % 1000) * 1000;

	do{
		ret = select(0, NULL, NULL, NULL, &tv);
	}while(ret < 0);
}

void doSomething()
{
	std::cout << "Timeout!" << std::endl;
}

int main()
{
	while(1)
	{
		SleepMs(1000); // 1000ms = 1s
		doSomething();
	}

	return 0;
}
