/*
 * Handler.h
 *
 *  Created on: Aug 7, 2016
 *      Author: eliwech
 */

#ifndef HANDLER_H_
#define HANDLER_H_

#include <string>

class Handler
{
public:
	Handler();
	virtual ~Handler();
	void setSuccessor(Handler *successor)
	{
		_successor = successor;
	}
	virtual std::string handleFeeRequest(std::string user, double fee) = 0;

protected:
	Handler *_successor;
};

class ProjectManager : public Handler
{
public:
	ProjectManager();
	virtual ~ProjectManager();
	virtual std::string handleFeeRequest(std::string user, double fee);
};

class DepManager : public Handler
{
public:
	DepManager();
	virtual ~DepManager();
	virtual std::string handleFeeRequest(std::string user, double fee);
};

class GeneralManager : public Handler
{
public:
	GeneralManager();
	virtual ~GeneralManager();
	virtual std::string handleFeeRequest(std::string user, double fee);
};

#endif /* HANDLER_H_ */
