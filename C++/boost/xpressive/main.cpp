//============================================================================
// Name        : Regex.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <iostream>
#include <string>
#include <boost/xpressive/xpressive_dynamic.hpp>



void shortMatch()
{
	boost::xpressive::cregex reg = boost::xpressive::cregex::compile("a.c");
	if (boost::xpressive::regex_match("abc", reg) && boost::xpressive::regex_match("a+c", reg))
	{
		std::cout << "short match" << std::endl;
	}

	if (!boost::xpressive::regex_match("ac", reg) && !boost::xpressive::regex_match("acd", reg))
	{
		std::cout << "short unmatch" << std::endl;
	}
}

void longMatch()
{
	/*
	 * \\d{6}:6 number element. eg:999555
	 * \\d{6}(1|2):6 number + 1 or 2. eg:9995551, 9995552
	 * \\d: just one number element
	 * [0-3]:one number. eg:0,1,2
	 * \\d{3}(X|\\d): 3 number element + X or one number. eg:999X or 9999
 	 */
	boost::xpressive::cregex reg = boost::xpressive::cregex::compile("\\d{6}(1|2)\\d{3}(0|1)\\d[0-3]\\d\\d{3}(X|\\d)", boost::xpressive::icase);

	if (   boost::xpressive::regex_match("999555197001019999", reg)
		&& boost::xpressive::regex_match("99955519700101999X", reg)
		&& boost::xpressive::regex_match("99955520100101999X", reg))
	{
		std::cout << "long match" << std::endl;
	}

	if (   !boost::xpressive::regex_match("99955520100101999Z", reg)
		&& !boost::xpressive::regex_match("99955530100101999X", reg)
		&& !boost::xpressive::regex_match("999555201099019998", reg)
		&& !boost::xpressive::regex_match("999555201012419991", reg))
	{
		std::cout << "long un_match" << std::endl;
	}
}

void fetchKeyWord()
{
	/*
	 * 8 sub_expression
	 * 0. \\d{6}((1|2)\\d{3})((0|1)\\d)([0-3]\\d)(\\d{3}(X|\\d))
	 * 1. ((1|2)\\d{3})
	 * 2. (1|2)
	 * 3. ((0|1)\\d)
	 * 4. (0|1)
	 * 5. ([0-3]\\d)
	 * 6. (\\d{3}(X|\\d))
	 * 7. (X|\\d)
	 */
	boost::xpressive::cregex reg = boost::xpressive::cregex::compile("\\d{6}((1|2)\\d{3})((0|1)\\d)([0-3]\\d)(\\d{3}(X|\\d))", boost::xpressive::icase);
	boost::xpressive::cmatch what;
	if (boost::xpressive::regex_match("999555197001019999", what, reg))
	{
		boost::xpressive::cmatch::iterator iter = what.begin();
		for(; iter!=what.end(); ++iter)
		{
			std::cout << "[" << *iter << "]";
		}
		std::cout << std::endl;

		std::cout << "data:" << what[1] << what[3] << what[5] << std::endl;
	}
}

void search()
{
	const char *str = "there is a POWER-suit item";
	boost::xpressive::cregex reg = boost::xpressive::cregex::compile("(power)-(.{4})", boost::xpressive::icase);
	if (boost::xpressive::regex_search(const_cast<char*>(str), reg))
	{
		std::cout << "search it" << std::endl;
	}

	/*
	 * 2 sub_expression
	 * 0. (power)
	 * 1. (.{4})
	 */
	boost::xpressive::cmatch what;
	if (boost::xpressive::regex_search(const_cast<char*>(str), what, reg))
	{
		if (what.size() == 3)
		{
			std::cout << what[1] << what[2] << std::endl;
		}
	}

	if (!boost::xpressive::regex_search("error message", reg))
	{
		std::cout << "error message unsearch" << std::endl;
	}
}


int main()
{
	/*short string totally match */
	shortMatch();

	/* long string totally match */
	longMatch();

	/* fetch keyword */
	fetchKeyWord();

	/* partly match and fetch keyword*/
	search();


	return 0;
}
