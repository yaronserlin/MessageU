#pragma once
#include <string>

class ClientData
{
	std::string _name;
	std::string _uniqueID;
	std::string _publicKey;
	std::string _symmetricKey;
public:
	void loadData(const std::string& name, const std::string& uniqueID, const std::string& privateKey);
	void setPublicKey(const std::string& publicKey);
	void setSymmetricKey(const std::string& symmetricKey);

	std::string getName();
	std::string getUniqueId();
	std::string getPublicKey();
	std::string getSymmetricKey();
};

