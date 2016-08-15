/*
 * StringUtil.h
 *
 *  Created on: 2016年2月11日
 *      Author: root
 */

#ifndef VERNAL_SERVER_STRINGUTIL_H_
#define VERNAL_SERVER_STRINGUTIL_H_

#include <string>

class StringUtil {
public:
	static std::string toLowerCase(std::string s);
	static std::string toUpperCase(std::string s);
};

#endif /* VERNAL_SERVER_STRINGUTIL_H_ */
