// C++
#include <cstring>
#include <iostream>
#include <thread>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/types.h>
// Chess
#include <ChessServer.hpp>


// C-tor
ChessServer::ChessServer() {

	// Create server socket
	serverSocket = ::socket(AF_INET, SOCK_STREAM, 0);
	// Failed ?
	if (serverSocket == -1) {

		// Throw exception
		throw std::system_error {
			std::make_error_code(std::errc::device_or_resource_busy),
			std::string {"Error creating server socket"}
		};

	}

	// Server address parameters
	serverAddress.sin_family = AF_INET;
	serverAddress.sin_addr.s_addr = INADDR_ANY;
	serverAddress.sin_port = ::htons(8080);

}

// D-tor
ChessServer::~ChessServer() {
	// Stop server
	ChessServer::stop();
}


// Start server
auto ChessServer::start() -> std::int32_t {

	// Bind server socket to server address
	if (::bind(serverSocket, reinterpret_cast<sockaddr*>(&serverAddress), sizeof(serverAddress)) == -1) {

		std::cerr << "Error binding server socket\n";

		return EXIT_FAILURE;

	}

	// Start waiting for connection
	if (::listen(serverSocket, ChessServer::MAX_CONNECTIONS) == -1) {

		std::cerr << "Error listening on server socket\n";
		return EXIT_FAILURE;

	}

	std::cout << "Chess server is listening on port 8080...\n";

	// Server loop
	while (true) {

		// Accept connection
		const auto clientSocket = ::accept(serverSocket, nullptr, nullptr);
		// Failed ?
		if (clientSocket == -1) {

			std::cerr << "Error accepting connection\n";

			// Try again
			continue;

		}

		std::cout << '[' << clientSocket << "]\tNew connection accepted\n";

		// Add client to clients list
		clientsList[clientSocket] = std::make_shared<ChessClient>(
			ChessClient {
				"",
				clientSocket
			}
		);

		// Client thread
		auto clientThread = std::thread {
			[this, clientSocket]() {

				// I/O buffer
				char buffer[8192] = {};
				// Read bytes count
				ssize_t bytesRead = 0;

				// Game code holder
				auto code = std::string {};

				// Connect loop
				while (true) {

					// Read data from client
					bytesRead = ::recv(clientSocket, buffer, sizeof(buffer), 0);

					// Nothing was read ?
					if (bytesRead <= 0) {
						// Stop loop
						break;
					}

					// Save game code
					code = std::string {buffer};
					// Cleanup I/O buffer
					std::memset(buffer, 0, sizeof(buffer));

					std::cout << '[' << clientSocket << "]\tClient code: \"" << code << "\"\n";

					// Client asked for new game ?
					if (code == std::string {"0"}) {

						// Save new game code
						code = std::to_string(clientSocket);
						// Create new pair for new game
						pairsList[code] = pair_t {
							clientsList[clientSocket],
							nullptr
						};

						std::cout << '[' << clientSocket << "]\tSession code: \"" << code << "\"\n";

						// Set data to send
						std::memcpy(buffer, code.data(), code.size());
						// Send data to client
						ssize_t bytesWrite = ::send(clientSocket, buffer, sizeof(buffer), 0);
						// Error check
						if (bytesWrite == 0) {
							// Stop loop
							break;
						}

						// Stop connect loop
						break;

					} else {

						// Game found ?
						if (pairsList.find(code) != pairsList.end()) {

							// Game waits for pair ?
							if (pairsList[code].second == nullptr) {

								// Add client to existing game
								pairsList[code].second = clientsList[clientSocket];

								std::cout << '\"' << code << "\"\tGame start\n";

								// Set data to "START"
								std::memcpy(buffer, "START", sizeof("START"));
								// Send data to client
								ssize_t bytesWrite = ::send(clientSocket, buffer, sizeof(buffer), 0);
								// Error check
								if (bytesWrite == 0) {
									// Stop loop
									break;
								}

							} else {

								// Set data to "UNKNOWN"
								std::memcpy(buffer, "UNKNOWN", sizeof("UNKNOWN"));
								// Send data to client
								ssize_t bytesWrite = ::send(clientSocket, buffer, sizeof(buffer), 0);
								// Error check
								if (bytesWrite == 0) {
									// Stop loop
									break;
								}

							}

							// Stop connect loop
							break;

						} else {

							// Set data to "UNKNOWN"
							std::memcpy(buffer, "UNKNOWN", sizeof("UNKNOWN"));
							// Send data to client
							ssize_t bytesWrite = ::send(clientSocket, buffer, sizeof(buffer), 0);
							// Error check
							if (bytesWrite == 0) {
								// Stop loop
								break;
							}

						}

					}

				}

				// Game loop
				while (true) {

					// Clean buffer
					std::memset(buffer, 0, sizeof(buffer));
					// Receive input from client
					bytesRead = ::recv(clientSocket, buffer, sizeof(buffer), 0);
					// Success ?
					if (bytesRead > 0) {

						// First client ?
						if (pairsList[code].first->socket == clientSocket) {
							// Send to second client
							ssize_t bytesWrite = ::send(pairsList[code].second->socket, buffer, bytesRead, 0);
							// Error check
							if (bytesWrite == 0) {
								// Stop loop
								break;
							}
						// Second client ?
						} else if (pairsList[code].second->socket == clientSocket) {
							// Send to first client
							ssize_t bytesWrite = ::send(pairsList[code].first->socket, buffer, bytesRead, 0);
							// Error check
							if (bytesWrite == 0) {
								// Stop loop
								break;
							}
						}

					} else {

						// Stop loop
						break;

					}


				}

				std::cout << '[' << clientSocket << "]\tClient disconnected\n";

				// Close client socket
				::close(clientSocket);

				// Remove client socket from list
				clientsList[clientSocket] = nullptr;

			}
		};

		// Run detached client socket
		clientThread.detach();

	}

	// Exit
	return 0;

}

// Stop server
void ChessServer::stop() {

	std::cout << "Error listening on server socket\n";

	// Close server socket
	::close(serverSocket);

}

