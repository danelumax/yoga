/*
 * UserManager.cpp
 *
 *  Created on: Oct 23, 2016
 *      Author: eliwech
 */

#include "UserManager.h"

typedef boost::tokenizer< boost::char_separator<char> > CustomTokenizer;

UserManager::UserManager()
{
}

UserManager::~UserManager()
{
}

std::vector<UserModelApi*> UserManager::getUserByDepId(std::string depId)
{
	std::vector<UserModelApi*> userModelvec;
    std::ifstream fin;
    fin.open("data.txt",std::ios::in);
    if(fin)
    {
        fin>>std::noskipws;
        std::string oneLine;

        while(getline(fin, oneLine, '\n'))
        {
            boost::char_separator<char> sep(" ");
            CustomTokenizer tok(oneLine, sep);
            CustomTokenizer::iterator iter = tok.begin();

            Proxy* proxy = new Proxy(new UserModel());
            proxy->setUserId(*(iter++));
            proxy->setName(*(iter++));

            if (*(iter++) == depId)
            {
            	userModelvec.push_back(proxy);
            }
            else
            {
            	delete proxy;
            }

        }
    }

    fin.close();

    return userModelvec;


}
