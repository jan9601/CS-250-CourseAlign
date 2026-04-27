import Sidebar from "./Sidebar";
import CalendarView from "./CalendarView";

function AppLayout() {
  return (
    <div className="grid grid-cols-[320px_1fr] h-screen">
      <Sidebar />
      <CalendarView />
    </div>
  );
}

export default AppLayout;
