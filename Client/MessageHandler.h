#pragma once
#include <string>
class MessageHandler {
public:
    std::string createMessage(const std::string& senderID, const std::string& recipientID, const std::string& messageType, const std::string& content);
    bool parseMessage(const std::string& message, std::string& senderID, std::string& recipientID, std::string& messageType, std::string& content);
    std::string encryptMessageWithPublicKey(const std::string& message, const std::string& publicKey);
    std::string decryptMessageWithPrivateKey(const std::string& encryptedMessage, const std::string& privateKey);
    std::string generateSymmetricKey();
};
