#pragma once
#include <string>
#include <set>

class Section {
private:
    std::string courseCode;
    std::string courseTitle;
    std::string sectionId;
    std::string component;
    std::string instructor;
    std::set<std::string> days;
    std::string startTime;
    std::string endTime;
    int units;
    std::string instructionMode;

public:
    Section(
        const std::string& courseCode,
        const std::string& courseTitle,
        const std::string& sectionId,
        const std::string& component,
        const std::string& instructor,
        const std::set<std::string>& days,
        const std::string& startTime,
        const std::string& endTime,
        int units,
        const std::string& instructionMode
    );

    std::string getCourseCode() const;
    std::string getCourseTitle() const;
    std::string getSectionId() const;
    std::string getComponent() const;
    std::string getInstructor() const;
    std::set<std::string> getDays() const;
    std::string getStartTime() const;
    std::string getEndTime() const;
    int getUnits() const;
    std::string getInstructionMode() const;
};
