/*
 * NdbOperationTransaction.cpp
 *
 *  Created on: Sep 9, 2016
 *      Author: eliwech
 */

#include <iostream>
#include "NdbOperationTransaction.h"
#include "NdbUtils.h"
#include "NdbClusterManager.h"


NdbOperationTransaction::NdbOperationTransaction()
	:_ndb(NULL), _ndbTrans(NULL)
{
}

NdbOperationTransaction::~NdbOperationTransaction()
{
	if (_ndbTrans != NULL)
	{
		_ndbTrans->close();
		_ndbTrans = NULL;
	}
}

int NdbOperationTransaction::startTransaction()
{
	_ndb = NdbClusterManager::getInstance()->getNdb();

	_ndbTrans = _ndb->startTransaction();

	return 0;
}

int NdbOperationTransaction::commitTransaction()
{
	NdbUtils::executeNdbTransaction(_ndbTrans,
									NdbTransaction::Commit,
									NdbOperation::AbortOnError);

	return 0;
}

NdbTransaction* NdbOperationTransaction::getNdbTransaction()
{
	return _ndbTrans;
}

Ndb* NdbOperationTransaction::getNdb()
{
	return _ndb;
}

void NdbOperationTransaction::close()
{
	if (_ndbTrans != NULL)
	{
		_ndbTrans->close();
		_ndbTrans = NULL;
	}

	if (_ndb != NULL)
	{
		NdbClusterManager::getInstance()->returnNdb(_ndb);
		_ndb = NULL;
	}
}


