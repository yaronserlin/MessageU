#include "NetworkManager.h"

//NetworkManager::_socket = tcp::socket(io_context);

NetworkManager::NetworkManager() : _io_context(), _socket(_io_context)
{
    _address = "";
    _port = "";
    //_socket = tcp::socket(io_context);

}

//NetworkManager::NetworkManager(const std::string& serverAddress, std::string serverPort) : _io_context(), _socket(_io_context)
//{
//    _address = serverAddress;
//    _port = serverPort;
//}

NetworkManager::~NetworkManager()
{
}

std::string NetworkManager::getAddress()
{
    return std::string(_address);
}

std::string NetworkManager::getPort()
{
    return _port;
}

void NetworkManager::setServerInfo(const std::string& address, const std::string& port)
{
    _address = address;
    _port = port;
}

tcp::socket& NetworkManager::connectToServer()
{
    try
    {
        boost::asio::io_context io_context;
        tcp::resolver resolver(io_context);
        boost::asio::connect(_socket, resolver.resolve(_address, _port));

        return _socket;
    }
    catch (const std::exception& e)
    {
        throw std::runtime_error("Connection error: " + std::string(e.what()));
    }
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
