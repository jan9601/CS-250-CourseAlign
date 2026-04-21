#include "Schedule.h"
#include <algorithm>

bool Schedule::canAdd(const Section& newClass) const {
    int totalUnits = 0;
    for (const Section& s : classes) {
        totalUnits += s.getUnits();
    }
    if (totalUnits + newClass.getUnits() > 21) {
        return false;
    }
    
    for (const Section& currClass : classes) {
        if (conflicts(currClass, newClass)) return false;
        if (currClass.getSectionId() == newClass.getSectionId()) return false;
        if (currClass.getCourseTitle() == newClass.getCourseTitle() &&
            currClass.getComponent() == newClass.getComponent()) return false;
    }
    return true;
}

void Schedule::add(const Section& section) {
    classes.push_back(section);
}

void Schedule::remove(const Section& section) {
    classes.erase(
        std::remove_if(classes.begin(), classes.end(),
                       [&](const Section& c) { return c.getSectionId() == section.getSectionId(); }),
        classes.end());
}

std::vector<Section> Schedule::getClasses() const {
    return classes;
}

bool conflicts(const Section& a, const Section& b) {
    // if either section has a TBD time (represented as "00:00"), assume no conflict
    if (a.getStartTime() == "00:00" || a.getEndTime() == "00:00" ||
        b.getStartTime() == "00:00" || b.getEndTime() == "00:00") {
        return false;
    }

    const std::set<std::string>& aDays = a.getDays();
    const std::set<std::string>& bDays = b.getDays();

    for (const std::string& day : aDays) {
        if (bDays.find(day) != bDays.end()) {
            // simple string comparison, assumes format "HH:MM"
            if (a.getStartTime() < b.getEndTime() &&
                b.getStartTime() < a.getEndTime()) {
                return true;
            }
        }
    }
    return false;
}
