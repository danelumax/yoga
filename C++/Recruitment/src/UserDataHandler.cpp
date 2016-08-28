#include <iostream>
#include <fstream>
#include <cstring>
#include <string>
#include "UserDataHandler.h"

UserDataHandler::UserDataHandler()
{
	_head = new UserDataList;
	_head->next = NULL;
}

UserDataHandler::~UserDataHandler()
{
}

//read the address information from file
void UserDataHandler::InitUserDataList()
{
    UserDataList *node, *h;
    std::string temp;
    std::ifstream fin;
    fin.open("data.txt",std::ios::in);
    std::cout << "The file is:" << std::endl;
    if(fin)
    {             
        fin>>std::noskipws;
        char *word = new char[100];
        while(!fin.eof())
        {  
            getline(fin, temp,'\n');
            strcpy(word, temp.c_str());
            char *p;
            p = strtok(word," ");
            int number = 0;
            std::string sa[3];
            while(p)
            {   
                sa[number++] = p;
                p = strtok(NULL, " ");   
            }
            h = _head;
            node = new UserDataList;
            for(int i=0; i<number; i++)
            {
                if(sa[i] == "\n")
                    std::cout <<"ok"<<std::endl;
            }
            node->name = sa[0];
            node->mobile = sa[1];
            node->address = sa[2];
            node->next = NULL;
            while(h->next)
                h = h->next;
            h->next = node;
        }
    }
    else
        std::cout <<"No data now!"<<std::endl;
    fin.close();
}

//display the address information in term of linked list
void UserDataHandler::Print()
{
    UserDataList *h;
    h = _head->next;
    while(h)
    {
        std::cout <<h->name<<" "<<h->mobile<<" "<<h->address<<std::endl;
        h = h->next;
    }
}

//Insert the address information into linked list
void UserDataHandler::InsertUserData()
{
    UserDataList *node, *h;
    h = _head;
    node = new UserDataList;
    std::cout <<"name:";
    std::cin>>node->name;
    std::cout <<"mobile:";
    std::cin>>node->mobile;
    std::cout <<"address:";
    std::cin>>node->address;
    node->next = NULL;   
    while(h->next)
        h = h->next;
    h->next = node;
}

//Write the address information into file
void UserDataHandler::WriteFile()
{
    UserDataList *h;
    h = _head->next;
    std::ofstream fout;
    fout.open("data.txt");
    if(h)
    {
        while(h->next)
        {
            fout<<h->name<<" "<<h->mobile<<" "<<h->address<<std::endl;
            h = h->next;
        }
            fout<<h->name<<" "<<h->mobile<<" "<<h->address;
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

//Search the address information from the linked list
void UserDataHandler::SearchUserData(std::string search_key, int search_id)
{
    UserDataList *h;
    h = _head;
    std::string result;
    std::string key = search_key;
    int count = 0;
    if(is_sub_str(search_key, ".*") == 1)
        key = key.substr(0, search_key.length()-strlen(".*"));
    while(h)
    {
        switch(search_id)
        {
            case 1:
                result = h->name;
                break;
            case 2:
                result = h->mobile;
                break;
            case 3:
                result = h->address;
                break;
        }
        if( is_sub_str(result, key) == 0 )
        {
            h = h->next;
        }
        else
        {
            std::cout <<h->name<<" "<<h->mobile<<" "<<h->address<<std::endl;
            count++;
            h = h->next;
        }
    }
    std::cout <<count<<" address entries searched"<<std::endl;
}

//Delete the address information from the linked list
void UserDataHandler::DeleteUserData(std::string search_key, int search_id)
{
    UserDataList *p, *h;
    h = _head->next;
    int count = 0;
    std::string result;
    std::string key = search_key;
    if(is_sub_str(search_key, ".*") == 1)
        key = key.substr(0, search_key.length()-strlen(".*"));
    while (h)
    {
        switch(search_id)
        {
            case 1:
                result = h->name;
                break;
            case 2:
                result = h->mobile;
                break;
            case 3:
                result = h->address;
                break;
        }
        if( is_sub_str(result, key) == 0 )
        {
            p = h;      
            h = h->next;
        }
        else
        {
            if ( h == _head->next)
            {
                _head->next = h ->next;
                delete h;
                h = _head->next;
                count++;
            } 
            else
            {              
                p->next=h->next;
                delete h;
                h = p->next;
                count++;
            } 
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
