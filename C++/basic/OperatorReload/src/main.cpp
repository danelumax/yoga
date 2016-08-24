//============================================================================
// Name        : OperatorReload.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <OperatorReload.h>

int main()
{
	OperatorReload *oprFirst = new OperatorReload("firstA", "firstB", "firstC");
	OperatorReload *oprSecond = new OperatorReload("secondA", "secondB", "secondC");
	OperatorReload *oprThird = new OperatorReload("thirdA", "thirdB", "thirdC");

	std::cout << "First Values: " << std::endl;
	oprFirst->showAllValue();

	std::cout << "\nAfter default assignment: " << std::endl;
	/* use default operator "=" */
	oprFirst = oprSecond;
	oprFirst->showAllValue();

	std::cout << "\nAfter reload assignment: " << std::endl;
	/* must use obj for calling reload operator "=" */
	*oprFirst = *oprThird;
	oprFirst->showAllValue();

	std::cout << "\nAfter reload addition: " << std::endl;
	((*oprFirst)+(*oprThird)).showAllValue();

	return 0;
}

