/*
 * ExportHeaderModel.h
 *
 *  Created on: Oct 17, 2016
 *      Author: eliwech
 */

#ifndef EXPORTHEADERMODEL_H_
#define EXPORTHEADERMODEL_H_

#include <string>

class ExportHeaderModel
{
public:
	ExportHeaderModel()
		: _depId(""), _exportDate("")
	{
	}

    std::string getDepId() const
    {
        return _depId;
    }

    std::string getExportDate() const
    {
        return _exportDate;
    }

    void setDepId(std::string depId)
    {
        _depId = depId;
    }

    void setExportDate(std::string exportDate)
    {
        _exportDate = exportDate;
    }

private:
	std::string _depId;
	std::string _exportDate;
};

#endif /* EXPORTHEADERMODEL_H_ */
