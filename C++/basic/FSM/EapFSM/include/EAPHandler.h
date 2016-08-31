/*
 * EAPHandler.h
 *
 *  Created on: Aug 31, 2016
 *      Author: eliwech
 */

#ifndef EAPHANDLER_H_
#define EAPHANDLER_H_

#include <EapFSM.h>
#include <DiaSessionContext.h>

class EAPHandler {
public:
	EAPHandler(DiaSessionContext* context);
	virtual ~EAPHandler();
	void Authentication();
	void Authorization();
private:
	EapFSM* _fsm;
	DiaSessionContext* _context;

};

#endif /* EAPHANDLER_H_ */
