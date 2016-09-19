/*
 * DiaSessionDataDBUtil.h
 *
 *  Created on: Sep 13, 2016
 *      Author: eliwech
 */

#ifndef DIASESSIONDATADBUTIL_H_
#define DIASESSIONDATADBUTIL_H_

class DiaSessionDataDBUtil {
public:
	static int insertSessionDataToDB();
	static int findSessionDatafromDB();
private:
	DiaSessionDataDBUtil(){};
};

#endif /* DIASESSIONDATADBUTIL_H_ */
