/*
 * ConfigModel.h
 *
 *  Created on: Oct 6, 2016
 *      Author: eliwech
 */

#ifndef CONFIGMODEL_H_
#define CONFIGMODEL_H_

class ConfigModel
{
public:
	ConfigModel();
	virtual ~ConfigModel();
	bool isNeedGenPresentation();
	bool isNeedGenBusiness();
	bool isNeed_needGenDAO();
private:
	bool _needGenPresentation;
	bool _needGenBusiness;
	bool _needGenDAO;
};

#endif /* CONFIGMODEL_H_ */
