
#include <MysqlDBManager.h>

int main()
{
	MysqlDBManager *manager = MysqlDBManager::getInstance();
	manager->initMysql();
	manager->connectMysql();
	manager->listAllData();

	return 0;
}
