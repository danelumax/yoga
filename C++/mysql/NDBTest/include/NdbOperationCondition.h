/*
 * NdbOperationCondition.h
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#ifndef NDBOPERATIONCONDITION_H_
#define NDBOPERATIONCONDITION_H_

#include <vector>
#include <NdbColumnCondition.h>

class NdbOperationCondition {
public:
	enum Type
	{
		INSERT = 1
	};
	NdbOperationCondition(Type type);
	virtual ~NdbOperationCondition();
	Type getType();
	bool isSingleRowOpearation();
	int addChangeColumn(NdbColumnCondition* column);
	std::vector<NdbColumnCondition*> getChangeColumns();
private:
	Type _type;
	std::vector<NdbColumnCondition*> _changeColumns;
};

#endif /* NDBOPERATIONCONDITION_H_ */
