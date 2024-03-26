# CMake versions range
cmake_minimum_required(
	VERSION
	3.1...3.28
)

# C++11 standard
set(
	CMAKE_CXX_STANDARD
	11
)
# Required C++ standard
set(
	CMAKE_CXX_STANDARD_REQUIRED
	True
)
# No GNU extensions!
set(
	CMAKE_CXX_EXTENSIONS
	OFF
)

# Includes path
include_directories(
	${CMAKE_SOURCE_DIR}
)

# GNU compiler flags
set(
	PROJECT_GNU_COMPILER_FLAGS
	-Wall # warn usefull warnings
	-Wextra # warn even more
	-Wconversion # warn on type conversions that may lose data
	-pedantic # warn if non-standard C++ is used
	-Werror # warnings as errors
)

# Compile options
add_compile_options(
	# Add compiler flags if Clang
	"$<$<CXX_COMPILER_ID:Clang>:${PROJECT_GNU_COMPILER_FLAGS}>"
	# Add compiler flags if GCC
	"$<$<CXX_COMPILER_ID:GNU>:${PROJECT_GNU_COMPILER_FLAGS}>"
)

# Project
project(
	ChessServer
	VERSION 1.0
	LANGUAGES CXX
)

# Thread
find_package(
	Threads REQUIRED
)

# Executable
add_executable(
	ChessServer
	ChessClient.hpp
	ChessClient.cpp
	ChessServer.hpp
	ChessServer.cpp
	main.cpp
)

# Dependencies
add_dependencies(
	ChessServer
	Threads::Threads
)

# Libraries
target_link_libraries(
	ChessServer
	PRIVATE
	Threads::Threads
)
