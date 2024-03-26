// C++
#include <iostream>
#include <system_error>
// Chess
#include <ChessServer.hpp>


// Entry point
int main() {

	// Try
	try {

		// Create server
		ChessServer server {};
		// Start server
		return server.start();

	}
	// Catch
	catch(const std::system_error &e) {

		// Print exception
		std::cerr << e.what();

		// Return exception code
		return e.code().value();

	}

}

