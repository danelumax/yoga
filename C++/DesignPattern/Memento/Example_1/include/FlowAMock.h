/*
 * FlowAMock.h
 *
 *  Created on: Sep 25, 2016
 *      Author: eliwech
 */

#ifndef FLOWAMOCK_H_
#define FLOWAMOCK_H_

#include <string>

class FlowAMockMemento
{
};

class FlowAMock
{
public:
	FlowAMock(std::string flowName);
	virtual ~FlowAMock();
	void runPhaseOne();
	void schema1();
	void schema2();
	FlowAMockMemento* createMemento();
	void setMemento(FlowAMockMemento* memento);
private:
	std::string _flowName;
	std::string _tempState;
	int _tempResult;
private:
	class MementoImpl : public FlowAMockMemento
	{
	public:
		MementoImpl(int tempImplResult, std::string tempImplState)
		{
			_tempImplResult = tempImplResult;
			_tempImplState = tempImplState;
		}
		int getImplTempResult()
		{
			return _tempImplResult;
		}
		std::string getImplTempState()
		{
			return _tempImplState;
		}
	private:
		int _tempImplResult;
		std::string _tempImplState;
	};
};

#endif /* FLOWAMOCK_H_ */
