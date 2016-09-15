/*
 * NdbOperationCondition.h
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#ifndef NDBOPERATIONCONDITION_H_
#define NDBOPERATIONCONDITION_H_

#include <vector>
#include <string>
#include <NdbColumnCondition.h>

class NdbOperationCondition {
public:
	enum Type
	{
		INSERT = 1
	};
	NdbOperationCondition(std::string tableName, Type type);
	virtual ~NdbOperationCondition();
	Type getType();
	bool isSingleRowOpearation();
	int addChangeColumn(NdbColumnCondition* column);
	std::vector<NdbColumnCondition*> getChangeColumns();
	std::string getTableName();
private:
	std::string _tableName;
	Type _type;
	std::vector<NdbColumnCondition*> _changeColumns;
};

#endif /* NDBOPERATIONCONDITION_H_ */
