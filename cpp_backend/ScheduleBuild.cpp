#include "ScheduleBuild.h"
#include <algorithm>
#include "Schedule.h"
#include "Section.h"
#include <vector>
#include <string>
#include <stdlib.h>
#include <iostream>
using namespace std;


vector<Section> getCourses(vector<Section> &sections, vector<string> courseTitles) {
    vector<Section> activeClasses;

    for (const Section &s: sections) {
        std::string code = s.getCourseCode();
	code.erase(std::remove(code.begin(), code.end(), ' '), code.end());
        for (const string &courseTitle: courseTitles) {
            if (courseTitle == code) {
                activeClasses.push_back(s);
            }
        }
    }

    return activeClasses;
}

bool checkExistence(Section course, vector<Section> &courses) {
    for (const Section &s: courses) {
        if (s.getCourseCode() == course.getCourseCode()) {
            return true;
        }
    }
    return false;
}

vector<Section> getEarliestStartTime(vector<Section> &activeClasses, string earliestStartTime) {
    // takes input start time as a string with format XX:XX, returns vector of sections excluding times earlier than that
    vector<Section> earliestStartTimes;
    vector<Section> unmetCourses;
    for (const Section &s: activeClasses) {
        if (s.getStartTime() >= earliestStartTime) {
            earliestStartTimes.push_back(s);
        }
        else {
            unmetCourses.push_back(s);
        }
    }

    vector<Section> trulyUnmet;
    for (const Section &s : unmetCourses) {
        if (!checkExistence(s, earliestStartTimes) && !checkExistence(s, trulyUnmet)) {
            trulyUnmet.push_back(s);
        }
    }

    if (!trulyUnmet.empty()) {
        cout << "No sections of ";
        for (int i = 0; i < trulyUnmet.size(); i++) {
            cout << trulyUnmet[i].getCourseCode();
            if (i != trulyUnmet.size() - 1) {
                cout << ", ";
            }
        }
        cout << " meet the specified start time preferences." << endl;
    }
    return earliestStartTimes;
}

vector<Section> getLatestEndTime(vector<Section>& activeClasses, string latestEndTime) {
    // takes input end time as a string with format XX:XX, returns vector of sections excluding times later than that
    vector<Section> latestEndTimes;
    vector<Section> unmetCourses;
    for (const Section& s : activeClasses) {
        if (s.getEndTime() <= latestEndTime) {
            latestEndTimes.push_back(s);
        }
        else {
            unmetCourses.push_back(s);
        }
    }

    vector<Section> trulyUnmet;
    for (const Section &s : unmetCourses) {
        if (!checkExistence(s, latestEndTimes) && !checkExistence(s, trulyUnmet)) {
            trulyUnmet.push_back(s);
        }
    }

    if (!trulyUnmet.empty()) {
        cout << "No sections of ";
        for (int i = 0; i < trulyUnmet.size(); i++) {
            cout << trulyUnmet[i].getCourseCode();
            if (i != trulyUnmet.size() - 1) {
                cout << ", ";
            }
        }
        cout << " meet the specified end time preferences." << endl;
    }
    return latestEndTimes;
}

#include <unordered_map>

vector<vector<Section>> splitCourses(vector<Section> activeCourses) {
    unordered_map<string, vector<Section>> groups;

    for (const Section& s : activeCourses) {
        string code = s.getCourseCode();
        code.erase(std::remove(code.begin(), code.end(), ' '), code.end());

        groups[code].push_back(s);
    }

    vector<vector<Section>> result;
    for (auto& pair : groups) {
        result.push_back(pair.second);
    }

    return result;
}

void recurseLoop(vector<Schedule>& schedules, vector<vector<Section>>& courses, int n, Schedule current) {
    //recursively checks all possible combinations of courses for conflicts, then adds them to a vector of schedules
    if (n >= courses.size()) {
        schedules.push_back(current);
        return;
    }
    for (int i = 0; i < courses[n].size(); i++) {
        Schedule currentLoop = current;
        if (currentLoop.canAdd(courses[n][i])) {
            currentLoop.add(courses[n][i]);
            recurseLoop(schedules, courses, n + 1, currentLoop);
        }
    }
}

vector<Schedule> createSchedules(vector<Section>& sections, vector<string> courseTitles, bool startPreference, bool endPreference, string earliestStartTime, string latestEndTime) {
    //creates a vector of valid schedules, takes a vector of all possible sections, vector of strings of the course titles, true/false arguments for the existence of a start/end time preference,
    //and the earliest possible start and end times as a string with format XX:XX (including padded zeros). returns a vector of all possible schedules with these parameters.
    vector<Section> activeCourses;
    vector<Schedule> schedules;
    vector<vector<Section>> groupedCourses;

    activeCourses = getCourses(sections, courseTitles);

    if (startPreference) {
	    activeCourses = getEarliestStartTime(activeCourses, earliestStartTime);
    }

    if (endPreference) {
	    activeCourses = getLatestEndTime(activeCourses, latestEndTime);
    }

    groupedCourses = splitCourses(activeCourses);

    if (groupedCourses.size() == 0) {
        return schedules;
    }

    int n = 0;
    Schedule current;

    recurseLoop(schedules, groupedCourses, n, current);
    return schedules;
}
