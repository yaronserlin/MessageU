#include <iostream>
#include "Log.h"
#include "FileManager.h"
#include "NetworkManager.h"
#include "UserInterface.h"

using std::string;

const string SERVER_INFO_FILE_PATH = "server.info";
const string USER_INFO_FILE_PATH = "my.info";

Log clientLog("client");

FileManager fManager;
NetworkManager nManager;
UserInterface UI;


void initializeConnection()
{
	//string address;
	//int port;
	try
	{
		clientLog.debug("Read server info");
		auto [address, port] = fManager.readServerInfo(SERVER_INFO_FILE_PATH);

		clientLog.debug("Saving server info in networkManager");
		nManager = NetworkManager(address, port);

		clientLog.debug("Server info: [" + nManager.getAddress() + ":" + std::to_string(nManager.getPort()) + "]");
	}
	catch (const std::exception& e)
	{
		clientLog.error("Error: " + string(e.what()));
	}
	

	

}
void sendMessage(const std::string& recipient, const std::string& message)
{

}
std::string receiveMessage()
{
	return "";
}
void run()
{

}


int main()
{
		

	initializeConnection();
	UI.displayWelcomeMessage();
	UI.displayMenu();
	string input;
	input = UI.getUserInput();
	if (!UI.isValidRequestNumber(input))
	{
		do {
			std::cout << "** Invalid choise. input must be one of the request option." << std::endl;
			//UI.displayMenu();
			input = UI.getUserInput();
		} while (!UI.isValidRequestNumber(input));
	}
	

	std::cout << "input [" + input + "] is valid!" << std::endl;





	return 0;
}
