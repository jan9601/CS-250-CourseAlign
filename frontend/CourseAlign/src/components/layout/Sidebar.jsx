import CourseSelector from "../../features/courses/CourseSelector";
import TimeFilters from "../../features/filters/TimeFIlters";
import ScheduleResults from "../../features/schedule/ScheduleResults";

function Sidebar() {
  return (
    <div className="bg-brand-dark w-full ">
      <img src="logo.png" className="h-30 w-30 mx-auto mt-5" />
      <div className="flex flex-col p-4 text-text-primary-light text-xs uppercase font-semibold">
        <CourseSelector />
        <TimeFilters />
        <ScheduleResults />
      </div>
    </div>
  );
}

export default Sidebar;
