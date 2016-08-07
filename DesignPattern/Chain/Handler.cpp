/*
 * Handler.cpp
 *
 *  Created on: Aug 7, 2016
 *      Author: eliwech
 */

#include <sstream>
#include "Handler.h"

Handler::Handler()
{
}

Handler::~Handler()
{
}

ProjectManager::ProjectManager()
{
}

ProjectManager::~ProjectManager()
{
}

std::string ProjectManager::handleFeeRequest(std::string user, double fee)
{
	std::ostringstream oss;
	std::string str("");
	if (fee < 500)
	{
		if ("Lee" == user)
		{
			oss << "ProjectManager approve " << user << " fee:" << fee;
		}
		else
		{
			oss << "ProjectManager reject " << user << " fee:" << fee;
		}
		return oss.str();
	}
	else
	{
		if (_successor != NULL)
		{
			return _successor->handleFeeRequest(user, fee);
		}
	}
	return oss.str();
}

DepManager::DepManager()
{
}

DepManager::~DepManager()
{
}

std::string DepManager::handleFeeRequest(std::string user, double fee)
{
	std::ostringstream oss;
	std::string str("");
	if (fee < 1000)
	{
		if ("Lee" == user)
		{
			oss << "DepManager approve " << user << " fee:" << fee;
		}
		else
		{
			oss << "DepManager reject " << user << " fee:" << fee;
		}
		return oss.str();
	}
	else
	{
		if (_successor != NULL)
		{
			return _successor->handleFeeRequest(user, fee);
		}
	}

	return oss.str();
}

GeneralManager::GeneralManager()
{
}

GeneralManager::~GeneralManager()
{
}

std::string GeneralManager::handleFeeRequest(std::string user, double fee)
{
	std::ostringstream oss;
	if (fee >= 1000)
	{
		if ("Lee" == user)
		{
			oss << "GeneralManager approve " << user << " fee:" << fee;
		}
		else
		{
			oss << "GeneralManager reject " << user << " fee:" << fee;
		}
		return oss.str();
	}
	else
	{
		if (_successor != NULL)
		{
			return _successor->handleFeeRequest(user, fee);
		}
	}

	return oss.str();
}
