#include <iostream>
#include "Log.h"
#include "FileManager.h"
#include "NetworkManager.h"
#include "UserInterface.h"
#include "ClientData.h"
#include "MessageHandler.h"
#include "SecurityManager.h"
#include <boost/asio.hpp>

using boost::asio::ip::tcp;

using std::string;

const string SERVER_INFO_FILE_PATH = "server.info";
const string USER_INFO_FILE_PATH = "my.info";

Log clientLog("client");


class Main
{
public:
	void initializeConnection();
	void sendMessage(const std::string& recipient, const std::string& message);
	std::string receiveMessage();
	void run();

private:
	FileManager fileManager;
	ClientData clientData;
	NetworkManager networkManager;
	MessageHandler messageHandler;
	SecurityManager securityManager;
	UserInterface userInterface;
};

void Main::initializeConnection()
{
	try
	{
		clientLog.debug("Read server info");
		auto [address, port] = fileManager.readServerInfo(SERVER_INFO_FILE_PATH);

		clientLog.debug("Saving server info in networkManager");
		networkManager.setServerInfo(address, port);
		clientLog.debug("Server info: [" + networkManager.getAddress() + ":" + networkManager.getPort() + "]");

		tcp::socket& socket = networkManager.connectToServer();

	}
	catch (const std::exception& e)
	{
		clientLog.error("Error: " + string(e.what()));
	}	

}
void Main::sendMessage(const std::string& recipient, const std::string& message)
{

}
std::string Main::receiveMessage()
{
	return "";
}
void Main::run()
{
	initializeConnection();
	userInterface.displayWelcomeMessage();
	userInterface.displayMenu();
	string input;
	input = userInterface.getUserInput();
	if (!userInterface.isValidRequestNumber(input))
	{
		do {
			std::cout << "** Invalid choise. input must be one of the request option." << std::endl;
			input = userInterface.getUserInput();
		} while (!userInterface.isValidRequestNumber(input));
	}


	std::cout << "input [" + input + "] is valid!" << std::endl;

}


int main() {
	Main program;
	program.run();
	return 0;
}
