/*
 * OptionState.h
 *
 *  Created on: Aug 28, 2016
 *      Author: eliwech
 */

#ifndef OPTIONSTATE_H_
#define OPTIONSTATE_H_

#include <UserDataHandler.h>

class OptionState
{
public:
	OptionState(UserDataHandler *handler);
	virtual ~OptionState();
	int getType();
	virtual void handle() = 0;
protected:
	UserDataHandler *_handler;
};

class AddState : public OptionState
{
public:
	AddState(UserDataHandler* handler);
	virtual ~AddState(){};
	virtual void handle();
};

class SearchState : public OptionState
{
public:
	SearchState(UserDataHandler* handler);
	virtual ~SearchState(){};
	virtual void handle();
};

class DeleteState : public OptionState
{
public:
	DeleteState(UserDataHandler* handler);
	virtual ~DeleteState(){};
	virtual void handle();
};

class ListAllState : public OptionState
{
public:
	ListAllState(UserDataHandler* handler);
	virtual ~ListAllState(){};
	virtual void handle();
};

class HelpState : public OptionState
{
public:
	HelpState(UserDataHandler* handler);
	virtual ~HelpState(){};
	virtual void handle();
};

class QuitState : public OptionState
{
public:
	QuitState(UserDataHandler* handler);
	virtual ~QuitState(){};
	virtual void handle();
};

#endif /* OPTIONSTATE_H_ */
