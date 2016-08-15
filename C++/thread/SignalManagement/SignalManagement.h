/*
 * SignalManagement.h
 *
 *  Created on: Aug 15, 2016
 *      Author: eliwech
 */

#ifndef SIGNALMANAGEMENT_H_
#define SIGNALMANAGEMENT_H_

#include <signal.h>

enum Flags
{
	KEEP_RUNNING = 0,
	EXIT = 1,
	MANAGED = 8
};

typedef struct SignalData
{
	int mask;
	void (*callback)(int);
}SignalData_t;

class SignalManagement
{
public:
	enum Flags
	{
		KEEP_RUNNING = 0,
		EXIT = 1,
		MANAGED = 8
	};
	static SignalManagement* getInstance();
	void destory();
	~SignalManagement();
	void signal(int sig, Flags flags, void(*callback)(int));
	void sigDefault(int sig);
	void sigIgnore(int sig);
	static void signalHandler(int sig, siginfo_t *siginfo, void *context);
private:
	SignalManagement();
	static SignalManagement* _instance;
	SignalData_t *_sigList;
};

#endif /* SIGNALMANAGEMENT_H_ */
