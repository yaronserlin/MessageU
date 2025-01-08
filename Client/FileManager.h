#pragma once
#include <string>
#include <vector>
#include <fstream>
#include <iostream>
#include <algorithm>

#include "Log.h"
class FileManager
{
private:
	static Log log;
	std::vector<std::string> readFromFile(const std::string& filePath);
public:
	std::pair<std::string, int> readServerInfo(const std::string& filePath);
	bool readClientData(const std::string& filePath, std::string& name, std::string& uniqueID, std::string& privateKey);
	bool writeClientData(const std::string& filePath, const std::string& name, const std::string& uniqueID, const std::string& privateKey);
	std::string generatePrivateKey();
};

