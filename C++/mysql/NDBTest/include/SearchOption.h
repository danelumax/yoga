/*
 * SearchOption.h
 *
 *  Created on: Sep 18, 2016
 *      Author: eliwech
 */

#ifndef SEARCHOPTION_H_
#define SEARCHOPTION_H_

#include <string>
#include <vector>

// for NDB
#define SEARCH_OPTION_QUERY_TYPE                "search_option_query_type"
#define SEARCH_OPTION_QUERY_TYPE_SINGLE_PK      "search_option_query_type_single_pk"

class SearchOption
{
public:
	enum CRITERIA_TYPE
	{
		CT_EQ = 0
	};

	typedef struct _SearchCriteria
	{
		std::string key;
		CRITERIA_TYPE type;
		std::string value;
	}SearchCriteria;

	SearchOption(std::string table);
	virtual ~SearchOption();

	std::string getTable();
	void addCriteria(std::string key, SearchOption::CRITERIA_TYPE ct, std::string value);
	int getCriteria(std::string key, std::string &value);
	std::vector<SearchOption::SearchCriteria*> getCriteriaVector();
	bool isHelpSearchKey(const std::string& key);

protected:
	std::string _table;
	std::vector<SearchOption::SearchCriteria*> _criteriaVector;
};

#endif /* SEARCHOPTION_H_ */
