/*
 * ResultSet.h
 *
 *  Created on: Sep 16, 2016
 *      Author: eliwech
 */

#ifndef RESULTSET_H_
#define RESULTSET_H_

#include <map>
#include <string>

class ResultSet
{
public:
	ResultSet();
	virtual ~ResultSet();
	void addValue(std::string key, std::string value);
private:
	std::map<std::string, std::string> _values;
};

#endif /* RESULTSET_H_ */
