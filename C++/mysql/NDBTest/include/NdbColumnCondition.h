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
	NdbColumnCondition(std::string columnName, int columnValue);
	virtual ~NdbColumnCondition();
	const char* getColumnName();
	int getColumnValue();
private:
	std::string _columnName;
	int _columnValue;
};

#endif /* NDBCOLUMNCONDITION_H_ */
