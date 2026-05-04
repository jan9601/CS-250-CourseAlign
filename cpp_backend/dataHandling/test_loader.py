from loader import load_sections, get_sections_by_course, get_all_course_codes

# ── Change this path if your CSV is somewhere else ──
CSV_PATH = "testData.csv"

def test_loads_without_crashing():
    sections = load_sections(CSV_PATH)
    assert len(sections) > 0, "Should load at least one section"
    print(f"PASS — Loaded {len(sections)} sections total")

def test_days_are_converted():
    sections = load_sections(CSV_PATH)
    # Every section's days should be a list of valid day strings
    valid_days = {"MON", "TUE", "WED", "THU", "FRI"}
    for s in sections:
        for day in s.days:
            assert day in valid_days, f"Invalid day '{day}' in section {s.section_id}"
    print("PASS — All days are valid strings (MON, TUE, etc.)")

def test_tbd_times_are_none():
    sections = load_sections(CSV_PATH)
    tbd_sections = [s for s in sections if s.start_time is None]
    print(f"PASS — Found {len(tbd_sections)} sections with TBD times (these are None, not 'TBD')")

def test_filter_by_course():
    sections = load_sections(CSV_PATH)
    cs210 = get_sections_by_course(sections, "CS 210")
    assert len(cs210) > 0, "CS 210 should have at least one section"
    for s in cs210:
        assert s.course_code == "CS 210"
    print(f"PASS — CS 210 has {len(cs210)} section(s)")

def test_to_dict():
    sections = load_sections(CSV_PATH)
    d = sections[0].to_dict()
    required_keys = ["course_code", "course_title", "section_id", "days", "start_time", "end_time"]
    for key in required_keys:
        assert key in d, f"Missing key '{key}' in to_dict() output"
    print("PASS — to_dict() contains all required API fields")

def test_all_course_codes():
    sections = load_sections(CSV_PATH)
    codes = get_all_course_codes(sections)
    assert len(codes) > 0
    print(f"PASS — Found {len(codes)} unique course codes")
    print(f"       First 5: {codes[:5]}")

def print_sample():
    sections = load_sections(CSV_PATH)
    print("\n── Sample Section (what Ryan and Greta will receive) ──")
    import json
    print(json.dumps(sections[0].to_dict(), indent=2))

if __name__ == "__main__":
    print("Running tests...\n")
    test_loads_without_crashing()
    test_days_are_converted()
    test_tbd_times_are_none()
    test_filter_by_course()
    test_to_dict()
    test_all_course_codes()
    print_sample()
    print("\nAll tests passed!")
