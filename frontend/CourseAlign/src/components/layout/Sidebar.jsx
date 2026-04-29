import CourseSelector from "../../features/courses/CourseSelector";
import TimeFilters from "../../features/filters/TimeFIlters";
import ScheduleResults from "../../features/schedule/ScheduleResults";

function Sidebar() {
  return (
    <aside className=" overflow-y-auto border-border/50 border-r">
      <img src="logo.png" className="h-30 w-30 mx-auto mt-2" />
      <div className="flex flex-col text-text-primary-light divide-y divide-border/50">
        <div className="px-4">
          <CourseSelector />
        </div>
        <div className="px-4">
          <TimeFilters />
        </div>
        <div className="px-4">
          <ScheduleResults />
        </div>
      </div>
    </aside>
  );
}

export default Sidebar;
