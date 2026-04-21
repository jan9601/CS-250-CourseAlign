#include "printSchedule.h"
#include <iostream>
#include <iomanip>
#include <sstream>
#include <algorithm>
#include <vector>

static const int W_CODE  = 10;
static const int W_TITLE = 26;
static const int W_SEC   = 10;
static const int W_COMP  = 10;
static const int W_DAYS  = 8;
static const int W_TIME  = 19;
static const int W_INST  = 18;
static const int W_UNITS = 5;
static const int W_MODE  = 10;

static std::string fit(const std::string& s, int width) {
    if ((int)s.size() <= width) return s;
    return s.substr(0, width - 2) + "..";
}

static std::string formatDays(const std::set<std::string>& days) {
    static const std::vector<std::string> order = {"M", "T", "W", "Th", "F"};
    std::string result;
    for (const auto& d : order) {
        if (days.count(d)) {
            if (!result.empty()) result += " ";
            result += d;
        }
    }
    return result.empty() ? "TBD" : result;
}

static int toMinutes(const std::string& t) {
    if (t.size() < 5) return -1;
    return std::stoi(t.substr(0, 2)) * 60 + std::stoi(t.substr(3, 2));
}

static std::string formatTime(const std::string& t) {
    if (t == "00:00" || t.empty()) return "TBD";
    int h = std::stoi(t.substr(0, 2));
    std::string min = t.substr(3, 2);
    std::string suffix = h >= 12 ? "pm" : "am";
    if (h > 12) h -= 12;
    if (h == 0) h = 12;
    return std::to_string(h) + ":" + min + suffix;
}

static void printDivider() {
    std::cout << "+"
        << std::string(W_CODE  + 2, '-') << "+"
        << std::string(W_TITLE + 2, '-') << "+"
        << std::string(W_SEC   + 2, '-') << "+"
        << std::string(W_COMP  + 2, '-') << "+"
        << std::string(W_DAYS  + 2, '-') << "+"
        << std::string(W_TIME  + 2, '-') << "+"
        << std::string(W_INST  + 2, '-') << "+"
        << std::string(W_UNITS + 2, '-') << "+"
        << std::string(W_MODE  + 2, '-') << "+"
        << "\n";
}

static void printRow(const std::string& code,
                     const std::string& title,
                     const std::string& sec,
                     const std::string& comp,
                     const std::string& days,
                     const std::string& time,
                     const std::string& inst,
                     const std::string& units,
                     const std::string& mode) {
    std::cout << "| " << std::left
        << std::setw(W_CODE)  << fit(code,  W_CODE)  << " | "
        << std::setw(W_TITLE) << fit(title, W_TITLE) << " | "
        << std::setw(W_SEC)   << fit(sec,   W_SEC)   << " | "
        << std::setw(W_COMP)  << fit(comp,  W_COMP)  << " | "
        << std::setw(W_DAYS)  << fit(days,  W_DAYS)  << " | "
        << std::setw(W_TIME)  << time                << " | "
        << std::setw(W_INST)  << fit(inst,  W_INST)  << " | "
        << std::setw(W_UNITS) << fit(units, W_UNITS) << " | "
        << std::setw(W_MODE)  << fit(mode,  W_MODE)  << " |"
        << "\n";
}

void printSchedule(const Schedule& s) {
    std::vector<Section> classes = s.getClasses();

    std::cout << "\n  === CourseAlign: Your Schedule ===\n\n";

    if (classes.empty()) {
        std::cout << "  No classes in this schedule.\n\n";
        return;
    }

    printDivider();
    printRow("Course", "Title", "Section", "Component", "Days", "Time", "Instructor", "Units", "Mode");
    printDivider();

    int totalUnits = 0;
    for (const Section& c : classes) {
        std::string timeStr = formatTime(c.getStartTime()) + " - " + formatTime(c.getEndTime());
        printRow(
            c.getCourseCode(),
            c.getCourseTitle(),
            c.getSectionId(),
            c.getComponent(),
            formatDays(c.getDays()),
            timeStr,
            c.getInstructor(),
            std::to_string(c.getUnits()),
            c.getInstructionMode()
        );
        totalUnits += c.getUnits();
    }

    printDivider();
    std::cout << "\n  Total Units: " << totalUnits << " / 21\n\n";
}

static const int CAL_TIME_W = 8;
static const int CAL_DAY_W  = 18;
static const int NUM_DAYS   = 5;
static const std::vector<std::string> DAY_KEYS   = {"M", "T", "W", "Th", "F"};
static const std::vector<std::string> DAY_LABELS = {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday"};

enum SepType { DOTTED, SOLID, CONTINUE };

static void printCalSeparator(const std::vector<SepType>& types) {
    std::cout << "+" << std::string(CAL_TIME_W + 2, '-') << "+";
    for (int d = 0; d < NUM_DAYS; d++) {
        if (types[d] == CONTINUE) {
            std::cout << std::string(CAL_DAY_W + 2, ' ') << "|";
        } else if (types[d] == SOLID) {
            std::cout << std::string(CAL_DAY_W + 2, '-') << "+";
        } else {
            std::string dot;
            for (int i = 0; i < CAL_DAY_W + 2; i++)
                dot += (i % 2 == 0) ? '-' : ' ';
            std::cout << dot << "+";
        }
    }
    std::cout << "\n";
}

static std::string center(const std::string& s, int width) {
    if ((int)s.size() >= width) return fit(s, width);
    int total = width - (int)s.size();
    int left  = total / 2;
    return std::string(left, ' ') + s + std::string(total - left, ' ');
}

void printCalendar(const Schedule& s) {
    std::vector<Section> classes = s.getClasses();

    std::cout << "\n  === CourseAlign: Weekly View ===\n\n";

    if (classes.empty()) {
        std::cout << "  No classes in this schedule.\n\n";
        return;
    }

    int earliest = 23 * 60, latest = 0;
    for (const Section& c : classes) {
        int start = toMinutes(c.getStartTime());
        int end   = toMinutes(c.getEndTime());
        if (start <= 0 || end <= 0) continue;
        if ((start / 30) * 30 < earliest) earliest = (start / 30) * 30;
        if (end > latest) latest = end;
    }
    earliest = std::max(0, (earliest / 30) * 30);
    latest   = std::min(23 * 60 + 30, ((latest + 29) / 30) * 30);

    std::vector<int> slots;
    for (int t = earliest; t < latest; t += 30)
        slots.push_back(t);
    int numSlots = (int)slots.size();

    std::vector<std::vector<int>> grid(numSlots, std::vector<int>(NUM_DAYS, -1));
    for (int si = 0; si < numSlots; si++) {
        for (int d = 0; d < NUM_DAYS; d++) {
            for (int ci = 0; ci < (int)classes.size(); ci++) {
                const Section& c = classes[ci];
                if (!c.getDays().count(DAY_KEYS[d])) continue;
                int start = toMinutes(c.getStartTime());
                int end   = toMinutes(c.getEndTime());
                if (start <= 0 || end <= 0) continue;
                if (start <= slots[si] && end > slots[si]) {
                    grid[si][d] = ci;
                    break;
                }
            }
        }
    }

    std::vector<std::vector<bool>> labelRow(numSlots, std::vector<bool>(NUM_DAYS, false));
    for (int d = 0; d < NUM_DAYS; d++) {
        int si = 0;
        while (si < numSlots) {
            int ci = grid[si][d];
            if (ci == -1) { si++; continue; }
            int blockStart = si;
            while (si < numSlots && grid[si][d] == ci) si++;
            labelRow[(blockStart + si - 1) / 2][d] = true;
        }
    }

    std::vector<SepType> allSolid(NUM_DAYS, SOLID);
    printCalSeparator(allSolid);

    std::cout << "| " << std::left << std::setw(CAL_TIME_W) << "Time" << " ";
    for (int d = 0; d < NUM_DAYS; d++)
        std::cout << "| " << std::setw(CAL_DAY_W) << center(DAY_LABELS[d], CAL_DAY_W) << " ";
    std::cout << "|\n";

    printCalSeparator(allSolid);

    for (int si = 0; si < numSlots; si++) {
        int h = slots[si] / 60, m = slots[si] % 60;
        int displayH = h > 12 ? h - 12 : (h == 0 ? 12 : h);
        std::ostringstream lbl;
        lbl << displayH << ":" << std::setw(2) << std::setfill('0') << m << (h >= 12 ? "pm" : "am");

        std::cout << "| " << std::left << std::setw(CAL_TIME_W) << lbl.str() << " ";

        for (int d = 0; d < NUM_DAYS; d++) {
            int ci = grid[si][d];
            std::string cell = "";
            if (ci != -1 && labelRow[si][d]) {
                std::string text = classes[ci].getCourseCode() + " " + classes[ci].getComponent();
                cell = center(fit(text, CAL_DAY_W), CAL_DAY_W);
            }
            std::cout << "| " << std::setw(CAL_DAY_W) << cell << " ";
        }
        std::cout << "|\n";

        if (si < numSlots - 1) {
            std::vector<SepType> types(NUM_DAYS);
            for (int d = 0; d < NUM_DAYS; d++) {
                if (grid[si][d] != -1 && grid[si][d] == grid[si + 1][d])
                    types[d] = CONTINUE;
                else if (grid[si][d] != -1 || grid[si + 1][d] != -1)
                    types[d] = SOLID;
                else
                    types[d] = DOTTED;
            }
            printCalSeparator(types);
        }
    }

    printCalSeparator(allSolid);
    std::cout << "\n";
}
