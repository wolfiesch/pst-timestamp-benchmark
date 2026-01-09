#include <cstdlib>
#include <ctime>
#include <iostream>

int main() {
    setenv("TZ", "America/Los_Angeles", 1);
    tzset();

    time_t now = time(nullptr);
    struct tm* local = localtime(&now);

    char buffer[64];
    strftime(buffer, sizeof(buffer), "%m/%d/%Y %I:%M %p %Z", local);
    std::cout << buffer << std::endl;
    return 0;
}
