const days = ["MON", "TUE", "WED", "THU", "FRI"];
const hours = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22];
function CalendarGrid() {
  return (
    <div className="grid grid-cols-[60px_repeat(5,1fr)] text-text-secondary-light mr-2 my-4">
      <div />
      {days.map((day) => (
        <div key={day} className="text-center text-xs font-medium py-2">
          {day}
        </div>
      ))}
      {hours.map((hour) => (
        <>
          <div key={hour} className="text-xs text-right pr-2 pt-1 opacity-50">
            {hour > 12 ? `${hour - 12}PM` : `${hour}AM`}
          </div>
          {days.map((day) => (
            <div key={day} className="border border-border min-h-15" />
          ))}
        </>
      ))}
    </div>
  );
}

export default CalendarGrid;
