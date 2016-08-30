/*
 * DiaSessionContext.h
 *
 *  Created on: Aug 30, 2016
 *      Author: eliwech
 */

#ifndef DIASESSIONCONTEXT_H_
#define DIASESSIONCONTEXT_H_

class DiaSessionContext
{
public:
	DiaSessionContext(){};
	~DiaSessionContext(){};
	void setState(int state)
	{
		_state = state;
	}
	int getState()
	{
		return _state;
	}
private:
	int _state;
};

#endif /* DIASESSIONCONTEXT_H_ */
