#include <iostream>
#include <string>
#include <mysql/mysql.h>

using namespace std;

int main()
{
    MYSQL mysql;
    MYSQL_RES *result = NULL;
    MYSQL_FIELD *field = NULL;
    mysql_init(&mysql);
    mysql_real_connect(&mysql, "localhost", "root", "rootroot", "test", 3306, NULL, 0); 
    string sql = "select id,name from t1;";
    mysql_query(&mysql, sql.c_str());
    result = mysql_store_result(&mysql);
    int rowcount = mysql_num_rows(result);
    cout << "rowcount:" << rowcount << endl;
    int fieldcount = mysql_num_fields(result);
    cout << "fieldcount:" << fieldcount << endl;
    for(int i = 0; i < fieldcount; i++)
    {
     field = mysql_fetch_field_direct(result,i);
     cout << field->name << "\t\t";
    }
    cout << endl;
    MYSQL_ROW row = NULL;
    row = mysql_fetch_row(result);
    while(NULL != row)
    {
     for(int i=0; i<fieldcount; i++)
     {
        cout << row[i] << "\t\t";
     }
     cout << endl;
     row = mysql_fetch_row(result);
    }
    mysql_close(&mysql);
}
