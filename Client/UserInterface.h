#pragma once
#include <string>

#include <iostream>
#include <algorithm>

#include "Log.h"
class UserInterface {
private:
    Log log = Log("UI");
public:
    bool isValidRequestNumber(std::string& input);
    void displayMenu();
    void displayWelcomeMessage();
    std::string getUserInput();
    void showMessage(const std::string& message);
};