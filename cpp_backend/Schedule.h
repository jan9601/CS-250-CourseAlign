#pragma once
#include <vector>
#include <string>
#include <set>
#include "Section.h"

class Schedule {
private:
    std::vector<Section> classes;

public:
    Schedule() = default;

    bool canAdd(const Section& newClass) const;
    void add(const Section& section);
    void remove(const Section& section);
    std::vector<Section> getClasses() const;
};

// conflict function declaration
bool conflicts(const Section& a, const Section& b);
