#include "Section.h"

Section::Section(
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
)
    : courseCode(courseCode),
      courseTitle(courseTitle),
      sectionId(sectionId),
      component(component),
      instructor(instructor),
      days(days),
      startTime(startTime),
      endTime(endTime),
      units(units),
      instructionMode(instructionMode)
{}

std::string Section::getCourseCode() const { return courseCode; }
std::string Section::getCourseTitle() const { return courseTitle; }
std::string Section::getSectionId() const { return sectionId; }
std::string Section::getComponent() const { return component; }
std::string Section::getInstructor() const { return instructor; }
std::set<std::string> Section::getDays() const { return days; }
std::string Section::getStartTime() const { return startTime; }
std::string Section::getEndTime() const { return endTime; }
int Section::getUnits() const { return units; }
std::string Section::getInstructionMode() const { return instructionMode; }
