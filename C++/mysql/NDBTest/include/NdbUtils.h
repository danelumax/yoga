/*
 * NdbUtils.h
 *
 *  Created on: Sep 7, 2016
 *      Author: eliwech
 */

#ifndef NDBUTILS_H_
#define NDBUTILS_H_

#include <NdbApi.hpp>

class NdbUtils {
public:
	static int executeNdbTransaction(NdbTransaction* &trans,
									 NdbTransaction::ExecType execType,
									 NdbOperation::AbortOption abortOp);
};

#endif /* NDBUTILS_H_ */
