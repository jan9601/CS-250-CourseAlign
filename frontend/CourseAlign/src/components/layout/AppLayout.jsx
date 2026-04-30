import Sidebar from "./Sidebar";
import CalendarView from "./CalendarView";

function AppLayout({
  courses,
  setCourses,
  earliestStart,
  setEarliestStart,
  latestEnd,
  setLatestEnd,
}) {
  return (
    <div className="grid grid-cols-[320px_1fr] h-screen bg-brand-dark-3">
      <Sidebar
        courses={courses}
        setCourses={setCourses}
        earliestStart={earliestStart}
        setEarliestStart={setEarliestStart}
        latestEnd={latestEnd}
        setLatestEnd={setLatestEnd}
      />
      <main className="overflow-y-auto h-screen ">
        <CalendarView />
      </main>
    </div>
  );
}

export default AppLayout;
