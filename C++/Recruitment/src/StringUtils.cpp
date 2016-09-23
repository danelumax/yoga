/*
 * StringUtils.cpp
 *
 *  Created on: Sep 23, 2016
 *      Author: eliwech
 */

#include "StringUtils.h"

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
