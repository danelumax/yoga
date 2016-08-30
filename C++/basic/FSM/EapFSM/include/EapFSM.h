/*
 * EapFSM.h
 *
 *  Created on: Aug 30, 2016
 *      Author: eliwech
 */

#ifndef EAPFSM_H_
#define EAPFSM_H_

#include <StateEventDefine.h>
#include <DiaSessionContext.h>
#include <StateTable.h>
#include <StateEntry.h>

class EapFSM
{
public:
	virtual ~EapFSM();
	static EapFSM* getInstance();
	static void destory();
	void init();
	void handleEvent(EPCEvent event, DiaSessionContext* context);
	StateEntry* matchState(EPCState state, EPCEvent event);
private:
	EapFSM();
	static EapFSM* _instance;
	StateTable *_stateTable;
};

#endif /* EAPFSM_H_ */
