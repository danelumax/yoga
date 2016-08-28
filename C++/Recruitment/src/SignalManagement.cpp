/*
 * SignalManagement.cpp
 *
 *  Created on: Aug 15, 2016
 *      Author: eliwech
 */

#include <iostream>
#include <memory.h>
#include "SignalManagement.h"

SignalManagement* SignalManagement::_instance = NULL;

SignalManagement::SignalManagement()
{
	_sigList = new SignalData_t[SIGRTMAX + 1];
	for(int i=0; i<SIGRTMAX+1; i++)
	{
		_sigList[i].mask = 0;
		_sigList[i].callback = 0;
	}
}

SignalManagement::~SignalManagement()
{
	/* set all signal to default */
	for(int i=0; i<SIGRTMAX+1; i++)
	{
		sigDefault(i);
	}

	delete[] _sigList;
	_sigList = NULL;
}

SignalManagement* SignalManagement::getInstance()
{
	if (_instance == NULL)
	{
		_instance = new SignalManagement();
	}

	return _instance;
}

void SignalManagement::destory()
{
	if (_instance != NULL)
	{
		delete _instance;
		_instance = NULL;
	}
}

/* Register signal */
void SignalManagement::signal(int sig, SignalManagement::Flags flags, void(*callback)(int))
{
	if (sig>SIGRTMAX || sig<0)
		return;

	// if flag=EXIT(1), mask=1001; if flag=KEEP_RUNNING(0), mask = 1000
	_sigList[sig].mask = MANAGED | ( (EXIT | KEEP_RUNNING) & flags );
	_sigList[sig].callback = callback;

	struct sigaction sa;
	memset(&sa, 0, sizeof(struct sigaction));
	/* if set SA_SIGINFO, system will use sigaction to be signal handling funtion */
	sa.sa_flags = SA_SIGINFO;
	/* set handling function */
	sa.sa_sigaction = SignalManagement::signalHandler;

	/* take effect */
	sigaction(sig, &sa, 0);
}

/* register signal before use this function */
void SignalManagement::sigDefault(int sig)
{
	if (sig>SIGRTMAX || sig<0)
		return;

	if (!(_sigList[sig].mask & MANAGED))
		return;

	/* use this signal default behavior */
	::signal(sig, SIG_DFL);

	_sigList[sig].mask = 0;
}

/* register signal before use this function */
void SignalManagement::sigIgnore(int sig)
{
	if (sig>SIGRTMAX || sig<0)
		return;

	if (!(_sigList[sig].mask & MANAGED))
		return;

	/* Ignore this signal, and do nothing */
	::signal(sig, SIG_IGN);

	_sigList[sig].mask = 0;
}

void SignalManagement::signalHandler(int sig, siginfo_t *siginfo, void *context)
{
	SignalManagement *me = SignalManagement::getInstance();
	Flags f_orig = (Flags)(me->_sigList[sig].mask);
	void (*cb_orig)(int) = me->_sigList[sig].callback;

	if (f_orig & EXIT) //1001 & 001 = 001
	{
		std::cout << "\nTrigger SignalHandler EXIT ! " << std::endl;
		_exit(sig); // non-normal exit like _exit(1)
	}
	if(cb_orig)
	{
		(cb_orig)(sig); // use callback function to handle this signal
	}
}
