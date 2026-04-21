#include "loadSections.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <set>
#include <stdexcept>

//make H:MM -> HH:MM
std::string normalizeTime(const std::string& time) {
    if (time == "TBD" || time.empty()) return "00:00";

    //add leading 0 if needed
    if (time.size() == 4) {
        return "0" + time;
    }

    return time;
}

std::set<std::string> parseDays(const std::string& raw) {
    std::set<std::string> days;
    for (size_t i = 0; i < 5 && i < raw.size(); i++) {
        if (raw[i] == 'c') {
            switch (i) {
                case 0: days.insert("M"); break;
                case 1: days.insert("T"); break;
                case 2: days.insert("W"); break;
                case 3: days.insert("Th"); break;
                case 4: days.insert("F"); break;
            }
        }
    }
    return days;
}

std::vector<std::string> split(const std::string& str, char delimiter) {
    std::vector<std::string> result;
    std::stringstream ss(str);
    std::string token;
    while (std::getline(ss, token, delimiter)) result.push_back(token);
    return result;
}

std::vector<Section> loadSectionsFromCsv(const std::string& path) {
    std::vector<Section> sections;
    std::ifstream file(path);
    if (!file.is_open()) throw std::runtime_error("Failed to open CSV file: " + path);

    std::string line;
    std::getline(file, line); // skip header
    int lineNumber = 1;

    while (std::getline(file, line)) {
        lineNumber++;
        std::vector<std::string> fields = split(line, ',');

        if (fields.size() < 11) {
            std::cerr << "Skipping invalid line " << lineNumber << std::endl;
            continue;
        }

        std::string courseCode = fields[1];
        std::string courseTitle = fields[2];
        std::string sectionId = fields[3];
        std::string component = fields[4];
        std::string instructor = fields[5];
        std::set<std::string> days = parseDays(fields[6]);

        std::string start = "00:00";
        std::string end = "00:00";

        if (!days.empty()) {
            start = normalizeTime(fields[7]);
            end = normalizeTime(fields[8]);
        }

        int units = 0;
        if (!fields[9].empty()) {
            try { 
                units = std::stoi(fields[9]); 
            } catch (...) { 
                std::cerr << "Invalid units at line " << lineNumber << std::endl; 
            }
        } else {
            std::cout << "Empty Units: " << lineNumber << std::endl;
        }

        std::string instructionMode = fields[10];

        sections.emplace_back(
            courseCode,
            courseTitle,
            sectionId,
            component,
            instructor,
            days,
            start,
            end,
            units,
            instructionMode
        );
    }

    return sections;
}
