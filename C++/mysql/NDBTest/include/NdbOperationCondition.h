/*
 * NdbOperationCondition.h
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#ifndef NDBOPERATIONCONDITION_H_
#define NDBOPERATIONCONDITION_H_

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
private:
	Type _type;
};

#endif /* NDBOPERATIONCONDITION_H_ */
