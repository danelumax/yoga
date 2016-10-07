//============================================================================
// Name        : AdapterLog.cpp
// Author      : 
// Version     :
// Copyright   : Your copyright notice
// Description : Hello World in C, Ansi-style
//============================================================================

#include <iostream>
#include "Adapter.h"
#include "LogFileOperate.h"

void listAll(std::vector<LogModel*> list)
{
	std::vector<LogModel*>::iterator iter = list.begin();
	for(list.begin(); iter!=list.end(); ++iter)
	{
		std::cout << (*iter)->getLogId() << " "
				  << (*iter)->getOperateUser() << " "
				  << (*iter)->getOperateTime() << " "
				  << (*iter)->getLogContent() << std::endl;
	}
}

int main()
{
	LogModel* lm1 = new LogModel();

	lm1->setLogId("001");
	lm1->setOperateUser("admin");
	lm1->setOperateTime("2010-03-02-10:08:18");
	lm1->setLogContent("this-is-a-test.");

	std::vector<LogModel*> list;
	LogFileOperateApi* logFileApi = new LogFileOperate();
	/* LogDbOperateApi --> LogFileOperateApi */
	LogDbOperateApi* api = new Adapter(logFileApi);

	std::cout << "Using DB Api ..." << std::endl;
	api->createLog(lm1);

	list = api->getAllLog();

	listAll(list);

	return 0;
}
