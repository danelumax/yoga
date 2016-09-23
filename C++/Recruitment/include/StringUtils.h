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
};

#endif /* STRINGUTILS_H_ */
