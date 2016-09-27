/*
 * StringUtils.cpp
 *
 *  Created on: Sep 23, 2016
 *      Author: eliwech
 */

#include "StringUtils.h"
#include <boost/algorithm/string.hpp>

StringUtils::StringUtils()
{
}

StringUtils::~StringUtils()
{
}

std::string StringUtils::toLowerCase(std::string needChangeStr)
{
	std::string ResultStr(needChangeStr.size(), char());
	for(unsigned int i = 0; i < needChangeStr.size(); ++i)
	{
		if (needChangeStr[i] <= 'Z' && needChangeStr[i] >= 'A')
		{
			ResultStr[i] = needChangeStr[i] + ('a'-'A');
		}
		else
		{
			ResultStr[i] = needChangeStr[i];
		}
	}

	return ResultStr;
}

int StringUtils::isSubStr(std::string str, std::string subStr)
{
	int ret = 0;
	boost::iterator_range<std::string::iterator> r = boost::algorithm::find_first(str, subStr);
	if (r.empty())
	{
		ret = 1;
	}

	return ret;
}
