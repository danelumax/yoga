//LinkedClass.h
//Class LinkedClass definition 

#ifndef USERDATAHANDLER_H
#define USERDATAHANDLER_H

#include <iostream>
#include <cstring>
#include <vector>
#include <Userdata.h>
#include <boost/pool/object_pool.hpp>

class UserDataHandler
{
public:
	UserDataHandler();
    ~UserDataHandler();

    void InitUserDataList();
    void Print();
    int InsertUserData();
    void WriteFile();
    void SearchUserData(std::string search_key, int search_id);
    void DeleteUserData(std::string search_key, int search_id);
    void ShowHelp();
    int CheckDelete(Userdata* userData);

private:
    std::vector<Userdata*> _userDataVec;
    boost::object_pool<Userdata> _pl;
};

#endif
