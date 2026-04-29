import Sidebar from "./Sidebar";
import CalendarView from "./CalendarView";

function AppLayout() {
  return (
    <div className="grid grid-cols-[320px_1fr] h-screen bg-brand-dark-3">
      <Sidebar />
      <main className="overflow-y-auto h-screen ">
        <CalendarView />
      </main>
    </div>
  );
}

export default AppLayout;
