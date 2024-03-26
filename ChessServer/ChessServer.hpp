#pragma once


// C++
#include <cstdint>
#include <memory>
#include <string>
#include <unordered_map>
#include <arpa/inet.h>
// Chess
#include <ChessClient.hpp>


// Client type declaration
using client_t = std::shared_ptr<ChessClient>;
// Clients pair type declaration
using pair_t = std::pair<std::shared_ptr<ChessClient>, std::shared_ptr<ChessClient>>;


// Chess server
class ChessServer {

	// Maximum number of connections
	constexpr static std::size_t MAX_CONNECTIONS = 64ULL;

	// Server socket
	std::int32_t	serverSocket	{};
	// Server address
	sockaddr_in	serverAddress	{};

	// Clients
	std::unordered_map<std::int32_t, client_t>	clientsList	{};
	// Client pairs
	std::unordered_map<std::string, pair_t>		pairsList	{};


public:

	// C-tor
	ChessServer();
	// D-tor
	~ChessServer();

	// Server start
	auto	start() -> std::int32_t;
	// Server stop
	void	stop();


};

