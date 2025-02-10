#include <cstdlib>
#include <iostream>
#include <fstream>
#include <errno.h>

#include "nlohmann/json.hpp"

#define BUFSIZE 4096

using json = nlohmann::json;

int main(int argc, char *argv[]) {
    std::istream *input;
    std::ifstream infile;
    std::string filename("");

    if (argc > 1) {
        filename = std::string(argv[1]);
    }

    if ((filename != "") && (filename != "-")) {
        infile.open(argv[1]);
        if (! infile.is_open()) {
            std::cerr << "Failed to open "
                      << argv[1]
                      << ": "
                      << strerror(errno)
                      << std::endl;
            return EXIT_FAILURE;
        }
        input = &infile;
    } else {
        input = &std::cin;
    }

    json j;
    *input >> j;
    std::cout << std::setw(4) << j << std::endl;

    return EXIT_SUCCESS;
}
