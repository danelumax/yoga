/*
 * ExportFooterModel.h
 *
 *  Created on: Oct 17, 2016
 *      Author: eliwech
 */

#ifndef EXPORTFOOTERMODEL_H_
#define EXPORTFOOTERMODEL_H_

#include <string>

class ExportFooterModel
{
public:
	ExportFooterModel()
		: _exportUser("")
	{
	}

    std::string getExportUser() const
    {
        return _exportUser;
    }

    void setExportUser(std::string exportUser)
    {
        _exportUser = exportUser;
    }

private:
	std::string _exportUser;
};

#endif /* EXPORTFOOTERMODEL_H_ */
