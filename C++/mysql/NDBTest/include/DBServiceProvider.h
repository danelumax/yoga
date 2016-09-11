/*
 * DBServiceProvider.h
 *
 *  Created on: Sep 11, 2016
 *      Author: eliwech
 */

#ifndef DBSERVICEPROVIDER_H_
#define DBSERVICEPROVIDER_H_

class DBServiceProvider
{
public:
	virtual ~DBServiceProvider();
	static DBServiceProvider* getInstance();
	static void destory();

private:
	DBServiceProvider();
	static DBServiceProvider* _instance;
};

#endif /* DBSERVICEPROVIDER_H_ */
