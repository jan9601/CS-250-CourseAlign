#include <iostream>
#include <algorithm>
#include <unordered_set>
#include <sstream>
#include <vector>
#include <regex>

#include "Section.h"
#include "ScheduleBuild.h"
#include "Schedule.h"
#include "dataHandling/loadSections.h"
#include "printSchedule.h"

int main() {
    try {
        std::vector<Section> sections = loadSectionsFromCsv("dataHandling/testData.csv");

        std::cout << "Welcome to CourseAlign!\n";

        std::cout << "Enter desired class list (e.g. MATH245 MATH254): ";
        std::string input;
        std::getline(std::cin, input);

        std::regex pattern("^([A-Z]+[0-9]+[A-Z]*)(\\s+[A-Z]+[0-9]+[A-Z]*)*$");
        if (!std::regex_match(input, pattern)) {
            std::cerr << "Invalid format. Example: MATH245 MATH254\n";
            return 1;
        }

        // Parse input
        std::vector<std::string> desiredCourses;
        std::istringstream iss(input);
        std::string course;

        while (iss >> course) {
            desiredCourses.push_back(course);
        }

        // Remove duplicates
        std::unordered_set<std::string> seen;
        std::vector<std::string> uniqueCourses;
        for (const std::string& c : desiredCourses) {
            if (seen.insert(c).second) {
                uniqueCourses.push_back(c);
            }
        }
        desiredCourses = uniqueCourses;

        // Validate against dataset
        std::unordered_set<std::string> validCourses;
        for (const Section& s : sections) {
		std::string code = s.getCourseCode();
		code.erase(remove(code.begin(), code.end(), ' '), code.end());
		validCourses.insert(code);
        }

        for (const std::string& c : desiredCourses) {
            if (validCourses.find(c) == validCourses.end()) {
                std::cerr << "Course not found: " << c << std::endl;
                return 1;
            }
        }

        // Preferences
        bool startPreference = false;
        bool endPreference = false;
        std::string earliestStartTime = "";
        std::string latestEndTime = "";

        std::regex timePattern("^([01][0-9]|2[0-3]):[0-5][0-9]$");

        std::cout << "Set earliest start time? (y/n): ";
        char startChoice;
        std::cin >> startChoice;

        if (startChoice == 'y' || startChoice == 'Y') {
            std::cout << "Enter earliest start time (HH:MM): ";
            std::cin >> earliestStartTime;

            if (!std::regex_match(earliestStartTime, timePattern)) {
                std::cerr << "Invalid time format.\n";
                return 1;
            }

            startPreference = true;
        }

        std::cout << "Set latest end time? (y/n): ";
        char endChoice;
        std::cin >> endChoice;

        if (endChoice == 'y' || endChoice == 'Y') {
            std::cout << "Enter latest end time (HH:MM): ";
            std::cin >> latestEndTime;

            if (!std::regex_match(latestEndTime, timePattern)) {
                std::cerr << "Invalid time format.\n";
                return 1;
            }

            endPreference = true;
        }

        // Generate schedules
        std::vector<Schedule> schedules = createSchedules(
            sections,
            desiredCourses,
            startPreference,
            endPreference,
            earliestStartTime,
            latestEndTime
        );

        // Output
        if (schedules.empty()) {
            std::cout << "No valid schedules found.\n";
        } else {
            std::cout << "\nFound " << schedules.size() << " valid schedule(s):\n\n";

            for (const Schedule& sched : schedules) {
                printSchedule(sched);
                printCalendar(sched);
            }
        }

    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
    }

    return 0;
}
