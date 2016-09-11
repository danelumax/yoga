/*
 * VernalNdbTransaction.cpp
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#include "VernalNdbTransaction.h"
#include <iostream>

VernalNdbTransaction::VernalNdbTransaction()
	:_ndbTrans(NULL)
{
	_ndbTrans = new NdbOperationTransaction();
}

VernalNdbTransaction::~VernalNdbTransaction()
{
}

int VernalNdbTransaction::start()
{
	if (_ndbTrans)
	{
		return _ndbTrans->startTransaction();
	}

	return 0;
}
