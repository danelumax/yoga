/*
 * XMLParse.cpp
 *
 *  Created on: 2016年2月2日
 *      Author: root
 */

#include "XMLParse.h"

XMLParse::XMLParse() {
	// TODO Auto-generated constructor stub

}

XMLParse::~XMLParse() {
	// TODO Auto-generated destructor stub
}

int XMLParse::ParseXMLFile()
{
	try{
		XMLPlatformUtils::Initialize();
	}
	catch (const XMLException& toCatch) {
		// Do your failure processing here
	    cout << "Initialize Error!" << endl;
	    return 1;
	}

	// Do your actual work with Xerces-C++ here.

	XercesDOMParser* parser = new XercesDOMParser();
	parser->setValidationScheme(XercesDOMParser::Val_Always);
	parser->setDoNamespaces(true);    // optional

	ErrorHandler* errHandler = (ErrorHandler*) new HandlerBase();
	parser->setErrorHandler(errHandler);

	//此处请用绝对路径
	const char* xmlFile = XML_FILE_PATH;

	try{
		parser->parse(xmlFile);
	}
	catch (const XMLException& toCatch){
		char* message = XMLString::transcode(toCatch.getMessage());
	    cout << "Exception message is: \n" << message << "\n";
	    XMLString::release(&message);
	    return -1;
	}
	catch (const DOMException& toCatch) {
		char* message = XMLString::transcode(toCatch.msg);
	    cout << "Exception message is: \n" << message << "\n";
	    XMLString::release(&message);
	    return -2;
	}
	catch (const SAXException& toCatch) {
		char* message = XMLString::transcode(toCatch.getMessage());
	    cout << "Exception message is: \n" << message << "\n";
	    XMLString::release(&message);
	    return -3;
	}
	catch (...) {
	    cout << "Unexpected Exception \n";
	    return -4;
	}



	//读取

	DOMDocument* doc = parser->getDocument();
	DOMNodeList* nodelist = doc->getChildNodes();
	DOMNode* root;
	DOMNodeList* childlist;
	DOMNode* child;
	DOMNode* attr;
	DOMNodeList* attrs;

	//最外层的 books
	for (unsigned int i = 0; i < nodelist->getLength(); i++)
	{
	    root = nodelist->item(i);
	    char *nodename = XMLString::transcode(root->getNodeName());
	    cout << nodename << endl;
	    XMLString::release(&nodename);
	    if (root->hasChildNodes())
	    {
	    	childlist = root->getChildNodes();
	    	//book
	    	for (unsigned int j = 1; j < childlist->getLength()-1; j+=2)
	    	{
	    		child = childlist->item(j);
	    		char *childname = XMLString::transcode(child->getNodeName());
	    		cout << "	" << childname << endl;
	    		XMLString::release(&childname);

	    		if (child->hasChildNodes())
	    		{
	    			attrs = child->getChildNodes();
	    			//name 等等
	    			for (unsigned int k = 1; k < attrs->getLength()-1; k+=2)
	    			{
	    				attr = attrs->item(k);
	    				char *attrname = XMLString::transcode(attr->getNodeName());
	    				char *attrvalue = XMLString::transcode(attr->getTextContent());

	    				cout << "		" << attrname << " : " << attrvalue << endl;
	    				XMLString::release(&attrname);
	    				XMLString::release(&attrvalue);

	    			}
	    		}
	    	}
	    }
	  }

	  delete parser;
	  delete errHandler;


	  XMLPlatformUtils::Terminate();

	  // Other terminations and cleanup.
	  return 0;
}

