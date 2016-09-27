/*
 * StringUtils.h
 *
 *  Created on: Sep 23, 2016
 *      Author: eliwech
 */

#ifndef STRINGUTILS_H_
#define STRINGUTILS_H_

#include <string>

class StringUtils
{
public:
	StringUtils();
	virtual ~StringUtils();
	static std::string toLowerCase(std::string needChangeStr);
	static int isSubStr(std::string str, std::string subStr);
};

#endif /* STRINGUTILS_H_ */
