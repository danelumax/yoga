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
	if (_ndbTrans)
	{
		_ndbTrans->close();

		delete _ndbTrans;
		_ndbTrans = NULL;
	}
}

int VernalNdbTransaction::start()
{
	if (_ndbTrans)
	{
		return _ndbTrans->startTransaction();
	}

	return 0;
}

int VernalNdbTransaction::commit()
{
	_ndbTrans->commitTransaction();

	return 0;
}

NdbOperationTransaction* VernalNdbTransaction::getNdbTransaction()
{
    return _ndbTrans;
}
