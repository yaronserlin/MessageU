#pragma once
#include <string>
class NetworkManager {
private:
    std::string _address;
    int _port;
public:
    NetworkManager();
    NetworkManager(const std::string& serverAddress, int serverPort);
    ~NetworkManager();

    std::string getAddress();
    int getPort();


    bool connectToServer(const std::string& serverAddress, int serverPort);
    bool requestPublicKeyFromServer(const std::string& clientID);
    bool sendMessageToServer(const std::string& message);
    std::string receiveMessageFromServer();
    bool sendEncryptedMessage(const std::string& recipient, const std::string& encryptedMessage);
    std::string decryptReceivedMessage(const std::string& encryptedMessage);
};

