#pragma once


// C++
#include <cstdint>
#include <string>


// Chess client description
struct ChessClient {

	// Client name
	std::string	name	{};
	// Client socket
	std::int32_t	socket	{};

	// C-tor
	ChessClient(const std::string &name, const std::int32_t socket);

};

