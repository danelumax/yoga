/*
 * Ndb.h
 *
 *  Created on: Sep 28, 2016
 *      Author: eliwech
 */

#ifndef NDB_H_
#define NDB_H_

class Ndb {
public:
	Ndb(int id);
	virtual ~Ndb();
	int getId();
private:
	int _id;
};

#endif /* NDB_H_ */
