/*
 * DiaSessionDataDBUtil.h
 *
 *  Created on: Sep 13, 2016
 *      Author: eliwech
 */

#ifndef DIASESSIONDATADBUTIL_H_
#define DIASESSIONDATADBUTIL_H_

#include "ResultSet.h"

class DiaSessionDataDBUtil {
public:
	static int insertSessionDataToDB();
	static int findSessionDatafromDB();
	static int deleteSessionDataInDB();
	static void sinkValueForSessionTable(ResultSet& record);
private:
	DiaSessionDataDBUtil(){};
};

#endif /* DIASESSIONDATADBUTIL_H_ */
