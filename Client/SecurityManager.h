#pragma once
#include <string>
class SecurityManager {
public:
    std::pair<std::string, std::string> generateRSAKeyPair();
    std::string encryptWithRSA(const std::string& data, const std::string& publicKey);
    std::string decryptWithRSA(const std::string& encryptedData, const std::string& privateKey);
    std::string encryptWithAES(const std::string& data, const std::string& symmetricKey);
    std::string decryptWithAES(const std::string& encryptedData, const std::string& symmetricKey);
};
