//============================================================================
// Name        : SignalManagement.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include "SignalManagement.h"
#include <iostream>

void doSomething(int sig)
{
	std::cout << "\nTrigger function doSometing ! " << std::endl;
	SignalManagement::getInstance()->sigDefault(sig);
}

int main(void)
{
	/* SIGINT means Ctrl+C */
	SignalManagement* sig = SignalManagement::getInstance();

	/*
	 * Scenario 1
	 * Register and set SIGINT do nothing
	 * Ignore SIGINT
	 * */
	sig->signal(SIGINT, SignalManagement::KEEP_RUNNING, 0);
	sig->sigIgnore(SIGINT);

	/*
	 * Scenario 2
	 * Register and set SIGINT default behavior
	 * */
	//sig->signal(SIGINT, SignalManagement::KEEP_RUNNING, 0);
	//sig->sigDefault(SIGINT);

	/*
	 * Scenario 3
	 * Register and set SIGINT using _exit(1) to exit
	 */
	//sig->signal(SIGINT, SignalManagement::EXIT, 0);

	/*
	 * Scenario 4
	 * Register and set SIGINT using doSomething to handle
	 * */
	//sig->signal(SIGINT, SignalManagement::KEEP_RUNNING, doSomething);

	sleep(100);
	return 0;
}
