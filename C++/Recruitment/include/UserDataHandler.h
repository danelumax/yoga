//LinkedClass.h
//Class LinkedClass definition 

#ifndef USERDATAHANDLER_H
#define USERDATAHANDLER_H

#include <iostream>
#include <cstring>

typedef struct node
{
    std::string name;
    std::string mobile;
    std::string address;
    struct node *next;
}UserDataList;

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
    UserDataList *_head;
};

#endif
