#include "UserInterface.h"


bool UserInterface::isValidRequestNumber(std::string& input)
{
	//if (input.empty() || !std::all_of(input.begin(), input.end(), ::isdigit)) {
	//	//throw std::runtime_error("Invalid port number in server info file. Port must be a numeric value.");
	//	log.error("Invalid input. Request input must be a numeric value.");
	//	return false;
	//}

	try
	{
		int intInput = std::stoi(input);

		switch (intInput)
		{
		case 110:
		case 120:
		case 130:
		case 140:
		case 150:
		case 151:
		case 152:
		case 153:
			return true;
		case 0:
			exit(0);
		default:
			log.error("Invalid input. Request [" + input + "] is not exsit.");
			return false;
		}
	}
	catch (const std::exception&)
	{
		log.error("Invalid input. Request input must be a numeric value.");
		return false;
	}
	
}

void UserInterface::displayMenu()
{
	std::cout << "110) Register" << std::endl;
	std::cout << "120) Request for clients list" << std::endl;
	std::cout << "130) Request for public key" << std::endl;
	std::cout << "140) Request for waiting messages" << std::endl;
	std::cout << "150) Send a text message" << std::endl;
	std::cout << "151) Send a request for symmetric key" << std::endl;
	std::cout << "152) Send your symmetric key" << std::endl;
	std::cout << "0) Exit client" << std::endl;
}

void UserInterface::displayWelcomeMessage()
{
	std::cout << "MessageU client at your service.\n" << std::endl;
}

std::string UserInterface::getUserInput()
{
	std::string input;
	std::cin >> input;

	

	return std::string(input);
}

void UserInterface::showMessage(const std::string& message)
{
}
