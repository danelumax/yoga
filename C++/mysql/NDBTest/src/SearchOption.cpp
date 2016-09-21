/*
 * SearchOption.cpp
 *
 *  Created on: Sep 18, 2016
 *      Author: eliwech
 */

#include "SearchOption.h"

SearchOption::SearchOption(std::string table)
	:_table(table)
{
}

SearchOption::~SearchOption()
{
	std::vector<SearchCriteria*>::iterator iter = _criteriaVector.begin();
	for(; iter!=_criteriaVector.end(); ++iter)
	{
		SearchCriteria* vqc = *iter;
		if (vqc)
		{
			delete vqc;
			vqc = NULL;
		}
	}
	_criteriaVector.clear();
}

std::string SearchOption::getTable()
{
	return _table;
}

void SearchOption::addCriteria(std::string key, CRITERIA_TYPE ct, std::string value)
{
	SearchCriteria* vqc = new SearchCriteria;
	vqc->key = key;
	vqc->type = ct;
	vqc->value = value;

	_criteriaVector.push_back(vqc);
}

int SearchOption::getCriteria(std::string key, std::string &value)
{
	std::vector<SearchOption::_SearchCriteria*>::iterator iter = _criteriaVector.begin();
	for(; iter!=_criteriaVector.end(); ++iter)
	{
		SearchOption::SearchCriteria* searchCriteria = *iter;
		if (searchCriteria && (searchCriteria->key).compare(key) == 0)
		{
			value = searchCriteria->value;
			return 0;
		}
	}

	return -1;
}

std::vector<SearchOption::SearchCriteria*> SearchOption::getCriteriaVector()
{
	return _criteriaVector;
}

bool SearchOption::isHelpSearchKey(const std::string& key)
{
	bool found = false;
	if (key.compare(SEARCH_OPTION_QUERY_TYPE) == 0)
	{
		found = true;
	}

	return found;
}

