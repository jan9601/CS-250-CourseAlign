# CourseAlign
CourseAlign is a C++ program that generates possible class schedules based on available course sections, avoiding time conflicts, and allowing students to view their schedules in a clean tabular format.

## Features
- Load course section data from CSV file
- Allow user to input prefered courses and start/end times of their day
- Generate all possible non-conflicting schedules
- Display schedules in a table format and calendar view

## Prerequisites
- C++17 or higher
- Make sure you have a C++ compiler like `g++`

## Installation / Usage
1. Clone the repository:
   git clone https://github.com/sleepymacaroni/CourseAlign.git
2. Navigate into the project folder:
   cd CourseAlign
3. Compile the project:
   g++ -std=c++17 -Wall -Wextra main.cpp Schedule.cpp Section.cpp printSchedule.cpp dataHandling/loadSections.cpp ScheduleBuild.cpp -o coursealign
4. Run the program:
   ./coursealign
5. Follow prompts to enter desired courses and time preferences

## Project Structure
- 'Section.h/cpp' – Defines course sections
- 'Schedule.cpp/h' – Defines schedules
- 'testData.csv' - Sample SDSU course data
- 'loadSections.cpp/h' – Loads data from CSV
- 'printSchedule.cpp/h' – Handles printing tables and calendar
- 'ScheduleBuild.cpp/h' - Handles assembly of schedules w/ user requirements
- 'main.cpp' – Main entry point

## Future Improvements
- Add GUI for easier schedule viewing and selection
- Use web scraping to aquire complete set of course data from SDSU
- Incorporate RateMyProfessor ratings / filtering by professor



## Authors
- Sasha Weingarten
- Christian Paper
- Zack Waterman
- Valeriia Stepanova