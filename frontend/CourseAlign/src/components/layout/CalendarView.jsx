import CalendarGrid from "../Calendar/CalendarGrid";
import CalendarHeader from "../Calendar/CalendarHeader";

function CalendarView() {
  return (
    <main className="flex flex-col h-screen">
      <CalendarHeader />
      <div className="overflow-y-auto flex-1">
        <CalendarGrid />
      </div>
    </main>
  );
}

export default CalendarView;
