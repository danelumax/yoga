#include <iostream>
#include <fstream>
#include <string>
#include <boost/format.hpp>
#include <boost/tokenizer.hpp>
#include <boost/algorithm/string.hpp>
#include "UserDataHandler.h"

typedef boost::tokenizer< boost::char_separator<char> > CustomTokenizer;

UserDataHandler::UserDataHandler()
{
}

UserDataHandler::~UserDataHandler()
{
}


void UserDataHandler::InitUserDataList()
{
    std::ifstream fin;
    fin.open("data.txt",std::ios::in);
    std::cout << "List all data:" << std::endl;
    if(fin)
    {             
        fin>>std::noskipws;
        std::string oneLine;
        while(getline(fin, oneLine, '\n'))
        {  
            boost::char_separator<char> sep(" ");
            CustomTokenizer tok(oneLine, sep);
            CustomTokenizer::iterator iter = tok.begin();

            Userdata *data = _pl.construct();
            data->setName(*(iter++));
			data->setMobile(*(iter++));
			data->setAddress(*(iter++));
			_userDataVec.push_back(data);
        }
    }

    fin.close();
}

//display the address information in term of linked list
void UserDataHandler::Print()
{
	if (_userDataVec.size() > 0)
	{
		std::vector<Userdata*>::iterator iter = _userDataVec.begin();
		for(; iter!=_userDataVec.end(); ++iter)
		{
			std::cout << (*iter)->getName() << " "
					  << (*iter)->getMobile() << " "
					  << (*iter)->getAddress() << std::endl;
		}
	}
	else
	{
		std::cout << "There is no data in the list" << std::endl;
	}
}

//Insert the address information into linked list
int UserDataHandler::InsertUserData()
{
	int ret = 0;
	std::string name(""), mobile(""), address("");
    std::cout << "name:";
    std::cin >> name;
    std::cout <<"mobile:";
    std::cin >> mobile;
    std::cout << "address:";
    std::cin >> address;

    /* protect quit program while add element */
    if (name!="" && mobile!="" && address!="")
    {
    	Userdata* data = _pl.construct();
    	data->setName(name);
    	data->setMobile(mobile);
    	data->setAddress(address);
    	_userDataVec.push_back(data);
    }
    else
    {
    	ret = 1;
    }
    return ret;
}

//Write the address information into file
void UserDataHandler::WriteFile()
{
    std::ofstream fout;
    fout.open("data.txt");

    std::vector<Userdata*>::iterator iter = _userDataVec.begin();
    for(; iter!=_userDataVec.end(); ++iter)
    {
    	fout << (*iter)->getName() << " "
    		 << (*iter)->getMobile() << " "
    		 << (*iter)->getAddress() << std::endl;
    }
    fout.close();
}

//judge similiar std::string
int is_sub_str(std::string str, std::string sub_str)
{
    int i,j,k;
    int len = sub_str.length();
    int flag = 0;
    char *str_char = new char;
    char *sub_str_char = new char;
    strcpy(str_char, str.c_str());
    strcpy(sub_str_char, sub_str.c_str());

    for(i=0; str_char[i]!=0; i+=k)
    {
        k = 1;
        for(j=0; sub_str_char[j]!=0; j++)
        {
            if(str_char[i+j] != sub_str_char[j])
                break;
        }
        if(j == len)
        {
            k = len;
            flag = 1;
        }
    }
    return flag;
}

void UserDataHandler::SearchUserData(std::string search_key, int search_id)
{
    std::string result;
    std::string key = search_key;
    int count = 0;
    if(is_sub_str(search_key, ".*") == 1)
        key = key.substr(0, search_key.length()-strlen(".*"));
    std::vector<Userdata*>::iterator iter = _userDataVec.begin();
    for(; iter!=_userDataVec.end(); ++iter)
    {
        switch(search_id)
        {
            case Userdata::NAME:
                result = (*iter)->getName();
                break;
            case Userdata::MOBILE:
                result = (*iter)->getMobile();
                break;
            case Userdata::ADDRESS:
                result = (*iter)->getAddress();
                break;
        }
        if( is_sub_str(result, key) != 0 )
        {
        	std::cout << (*iter)->getName() << " "
        			  << (*iter)->getMobile() << " "
        			  << (*iter)->getAddress() << std::endl;
            count++;
        }
    }
    std::cout <<count<<" address entries searched"<<std::endl;
}


void UserDataHandler::DeleteUserData(std::string search_key, int search_id)
{
    int count = 0;
    std::string result;
    std::string key = search_key;
    if(is_sub_str(search_key, ".*") == 1)
        key = key.substr(0, search_key.length()-strlen(".*"));

    std::vector<Userdata*>::iterator iter = _userDataVec.begin();
    /* don't add ++iter */
    for(; iter!=_userDataVec.end();)
    {
        switch(search_id)
        {
            case 1:
                result = (*iter)->getName();
                break;
            case 2:
                result = (*iter)->getMobile();
                break;
            case 3:
                result = (*iter)->getAddress();
                break;
        }
        if( is_sub_str(result, key) != 0 )
        {
        	/* point to next element, must be set */
        	iter = _userDataVec.erase(iter);
            count++;
        }
        else
        {
        	iter++;
        }
    }

    std::cout <<count<<" address entries deleted"<<std::endl;
}

//Show help message
void UserDataHandler::ShowHelp()
{
    std::cout <<"help message"<<std::endl;
    std::cout <<"#add  this order is used to add relevent information"<<std::endl;
    std::cout <<"#search  this order is used to search relevent information"<<std::endl;
    std::cout <<"#delete  this order is used to delete relevent information"<<std::endl;
    std::cout <<"#dispaly  this order is used to display relevent information"<<std::endl;
}
