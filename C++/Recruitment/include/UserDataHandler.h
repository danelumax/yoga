//LinkedClass.h
//Class LinkedClass definition 

#ifndef USERDATAHANDLER_H
#define USERDATAHANDLER_H

#include <iostream>
#include <cstring>
#include <vector>
#include <Userdata.h>

class UserDataHandler
{
public:
	UserDataHandler();
    ~UserDataHandler();

    void InitUserDataList();
    void Print();
    void InsertUserData();
    void WriteFile();
    void SearchUserData(std::string search_key, int search_id);
    void DeleteUserData(std::string search_key, int search_id);
    void ShowHelp();

private:
    std::vector<Userdata*> _userDataVec;
};

#endif
