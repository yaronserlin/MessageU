#include "FileManager.h"

Log FileManager::log = Log("FileManager");

std::vector<std::string> FileManager::readFromFile(const std::string& filePath)
{
    {
        std::vector<std::string> lines;
        std::ifstream file(filePath);

        if (!file) {
            throw std::runtime_error("Unable to open file: " + filePath);
        }

        std::string line;
        while (std::getline(file, line)) {
            lines.push_back(line); // Add each line to the vector.
        }

        file.close();
        return lines;
    }
}

std::pair<std::string, std::string> FileManager::readServerInfo(const std::string & filePath)
{   
    std::vector<std::string> lines = readFromFile(filePath);
    std::string serverAddress;
    std::string port;

    if (lines.empty())
        throw std::runtime_error("Failed to read server info file.");

    std::string line = lines[0];

    size_t pos = line.find(':');
    if (pos == std::string::npos) {
        throw std::runtime_error("Invalid server info format. Expected format: <IP>:<PORT>");
    }

    serverAddress = line.substr(0, pos);

    // Extract the port substring
    std::string portStr = line.substr(pos + 1);

    // Validate that the port string is numeric
    if (portStr.empty() || !std::all_of(portStr.begin(), portStr.end(), ::isdigit)) {
        throw std::runtime_error("Invalid port number in server info file. Port must be a numeric value.");
    }

    try {
        port = std::stoi(portStr);
    }
    catch (const std::out_of_range&) {
        throw std::runtime_error("Port number out of range in server info file.");
    }
    return { serverAddress,portStr };
}

bool FileManager::readClientData(const std::string& filePath, std::string& name, std::string& uniqueID, std::string& privateKey)
{
    // TODO: Add your implementation code here.
    return true;
}


bool FileManager::writeClientData(const std::string& filePath, const std::string& name, const std::string& uniqueID, const std::string& privateKey)
{
    // TODO: Add your implementation code here.
    return true;
}


std::string FileManager::generatePrivateKey()
{
    // TODO: Add your implementation code here.
    return std::string();
}
