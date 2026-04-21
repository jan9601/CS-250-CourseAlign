// ScheduleBuild.h
#pragma once
#include "Schedule.h"
#include "Section.h"
#include <vector>
#include <string>
using namespace std;

// Function declarations
vector<Section> getCourses(vector<Section>& sections, vector<string> courseTitles);
bool checkExistence(Section course, vector<Section> &courses);
vector<Section> getEarliestStartTime(vector<Section>& activeClasses, string earliestStartTime);
vector<Section> getLatestEndTime(vector<Section>& activeClasses, string latestEndTime);
vector<vector<Section>> splitCourses(vector<Section> activeCourses);
void recurseLoop(vector<Schedule>& schedules, vector<vector<Section>>& courses, int n, Schedule current);
vector<Schedule> createSchedules(vector<Section>& sections, vector<string> courseTitles, bool startPreference, bool endPreference, string earliestStartTime, string latestEndTime);