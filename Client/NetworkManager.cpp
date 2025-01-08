#include "NetworkManager.h"

NetworkManager::NetworkManager()
{
    _address = "";
    _port = 0;
}

NetworkManager::NetworkManager(const std::string& serverAddress, int serverPort)
{
    _address = serverAddress;
    _port = serverPort;
}

NetworkManager::~NetworkManager()
{
}

std::string NetworkManager::getAddress()
{
    return std::string(_address);
}

int NetworkManager::getPort()
{
    return _port;
}

bool NetworkManager::connectToServer(const std::string& serverAddress, int serverPort)
{
    return false;
}

bool NetworkManager::requestPublicKeyFromServer(const std::string& clientID)
{
    return false;
}

bool NetworkManager::sendMessageToServer(const std::string& message)
{
    return false;
}

std::string NetworkManager::receiveMessageFromServer()
{
    return std::string();
}

bool NetworkManager::sendEncryptedMessage(const std::string& recipient, const std::string& encryptedMessage)
{
    return false;
}

std::string NetworkManager::decryptReceivedMessage(const std::string& encryptedMessage)
{
    return std::string();
}
