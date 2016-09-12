/*
 * NdbDao.cpp
 *
 *  Created on: Sep 12, 2016
 *      Author: eliwech
 */

#include "NdbDao.h"
#include <iostream>
#include "NdbOperationCondition.h"
#include "NdbAbstractExecutor.h"

NdbDao::NdbDao() {
	// TODO Auto-generated constructor stub

}

NdbDao::~NdbDao() {
	// TODO Auto-generated destructor stub
}

int NdbDao::insert(int i)
{
	NdbOperationCondition noc(NdbOperationCondition::INSERT);
	NdbAbstractExecutor executor(noc, NULL);
	executor.execute(i);
}


