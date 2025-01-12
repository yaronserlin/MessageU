#pragma once
#include <string>

#include <boost/asio.hpp>

using boost::asio::ip::tcp;


class NetworkManager {
private:
    std::string _address;
    std::string _port;
    boost::asio::io_context _io_context;
    tcp::socket _socket;
public:
    NetworkManager();
    ~NetworkManager();
    std::string getAddress();
    std::string getPort();

    void setServerInfo(const std::string& address, const std::string& port);


    tcp::socket& connectToServer();
    bool requestPublicKeyFromServer(const std::string& clientID);
    bool sendMessageToServer(const std::string& message);
    std::string receiveMessageFromServer();
    bool sendEncryptedMessage(const std::string& recipient, const std::string& encryptedMessage);
    std::string decryptReceivedMessage(const std::string& encryptedMessage);
};

