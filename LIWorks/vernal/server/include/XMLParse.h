/*
 * XMLParse.h
 *
 *  Created on: 2016年2月2日
 *      Author: root
 */

#ifndef XMLPARSE_H_
#define XMLPARSE_H_

#include <xercesc/util/PlatformUtils.hpp>
#include <xercesc/parsers/XercesDOMParser.hpp>
#include <xercesc/dom/DOM.hpp>
#include <xercesc/sax/HandlerBase.hpp>
#include <xercesc/util/XMLString.hpp>
#include <iostream>

#define XML_FILE_PATH "../book.xml"

// Other include files, declarations, and non-Xerces-C++ initializations.
using namespace xercesc;
using namespace std;

class XMLParse {
public:
	XMLParse();
	virtual ~XMLParse();
	int ParseXMLFile();
};

#endif /* XMLPARSE_H_ */
