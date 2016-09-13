/*
 * NdbOperationTransaction.cpp
 *
 *  Created on: Sep 9, 2016
 *      Author: eliwech
 */

#include <iostream>
#include "NdbOperationTransaction.h"
#include "NdbClusterManager.h"

#define PRINT_ERROR(code,msg) \
  std::cout << "Error in " << __FILE__ << ", line: " << __LINE__ \
            << ", code: " << code \
            << ", msg: " << msg << "." << std::endl
#define APIERROR(error) {PRINT_ERROR(error.code,error.message); _exit(-1);}

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

NdbTransaction* NdbOperationTransaction::getNdbTransaction()
{
	return _ndbTrans;
}

Ndb* NdbOperationTransaction::getNdb()
{
	return _ndb;
}


