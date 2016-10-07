/*
 * LogFileOperate.cpp
 *
 *  Created on: Oct 7, 2016
 *      Author: eliwech
 */

#include "LogFileOperate.h"
#include <fstream>
#include <boost/format.hpp>
#include <boost/tokenizer.hpp>
#include <boost/algorithm/string.hpp>

typedef boost::tokenizer< boost::char_separator<char> > CustomTokenizer;

LogFileOperate::LogFileOperate()
	: _logFilePathName("AdapterLog.log")
{
}

LogFileOperate::~LogFileOperate()
{
}

std::vector<LogModel*> LogFileOperate::readLogFile()
{
	std::vector<LogModel*> list;
    std::ifstream fin;
    fin.open(_logFilePathName.c_str(), std::ios::in);
    if(fin)
    {
        fin>>std::noskipws;
        std::string oneLine;
        while(getline(fin, oneLine, '\n'))
        {
            boost::char_separator<char> sep(" ");
            CustomTokenizer tok(oneLine, sep);
            CustomTokenizer::iterator iter = tok.begin();

            LogModel* data = new LogModel();

			data->setLogId(*(iter++));
			data->setOperateUser(*(iter++));
			data->setOperateTime(*(iter++));
			data->setLogContent(*(iter++));

			list.push_back(data);
        }
    }

    fin.close();

    return list;
}

void LogFileOperate::writeLogFile(std::vector<LogModel*> list)
{
    std::ofstream fout;
    fout.open(_logFilePathName.c_str());

    std::vector<LogModel*>::iterator iter = list.begin();
    for(; iter!=list.end(); ++iter)
    {
    	fout << (*iter)->getLogId() << " "
    		 << (*iter)->getOperateUser() << " "
    		 << (*iter)->getOperateTime() << " "
    		 << (*iter)->getLogContent() << std::endl;
    }
    fout.close();
}
