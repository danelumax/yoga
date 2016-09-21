/*
 * NdbUtils.h
 *
 *  Created on: Sep 7, 2016
 *      Author: eliwech
 */

#ifndef NDBUTILS_H_
#define NDBUTILS_H_

#include <NdbApi.hpp>
#include <NdbOperationCondition.h>
#include <NdbColumnCondition.h>
#include <NdbAbstractExecutor.h>

class NdbUtils {
public:
	static int executeNdbTransaction(NdbTransaction* &trans,
									 NdbTransaction::ExecType execType,
									 NdbOperation::AbortOption abortOp);

	static int setNdbOperationType(NdbOperationCondition* opCondition,
						    const NdbDictionary::Table * &myTable,
	                        NdbTransaction* &myTrans,
	                        NdbOperation * &myOp);

	static int setNdbOperationActivity(NdbOperation * &oper, NdbOperationCondition& noc);

	static int prepareKeyNdbSingleOp(NdbOperation* oper, NdbOperationCondition* opCondition);

	static int setKeyNdbOperationInfo(NdbOperation * &myOp, NdbColumnCondition* cqf);

	static int prepareNdbOperationValues(NdbOperation* myOp, NdbOperationCondition* opCondition);

	static int prepareNdbOperationQuerySpace(NdbOperation* oper,
											 NdbOperationCondition* opCondition,
											 NdbAbstractExecutor* queryExecutor);

	static bool isValidColumnName(const std::string& columnName);


};

#endif /* NDBUTILS_H_ */
