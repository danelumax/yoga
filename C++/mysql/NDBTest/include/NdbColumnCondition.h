/*
 * NdbColumnCondition.h
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#ifndef NDBCOLUMNCONDITION_H_
#define NDBCOLUMNCONDITION_H_

#include <string>

class NdbColumnCondition
{
public:
	enum Condition
	{
		COND_EQ = 0
	};
	NdbColumnCondition(std::string columnName,
					   std::string columnValue,
					   NdbColumnCondition::Condition op = NdbColumnCondition::COND_EQ);
	virtual ~NdbColumnCondition();
	const char* getColumnName();
	std::string getColumnValue();
private:
	std::string _columnName;
	std::string _columnValue;
	NdbColumnCondition::Condition _op;
};

#endif /* NDBCOLUMNCONDITION_H_ */
