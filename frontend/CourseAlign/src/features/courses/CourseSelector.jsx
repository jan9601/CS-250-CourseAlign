import {FiPlus, FiX} from "react-icons/fi";

function CourseSelector() {
  const isCourseAdded = true;
  const coursesAddedList = ["CS 250", "CS 350", "MATH 250"];
  return (
    <div className="mb-5">
      <form className="p-2">
        <p className="opacity-65 mb-2 text-[14px] font-semibold uppercase">
          Courses
        </p>
        <div className="relative">
          <input
            placeholder="Search for courses... (CS 250)"
            className="h-9 pr-10 pl-2 placeholder:text-xs rounded-lg bg-surface placeholder:text-text-secondary-dark/70 w-full text-text-primary-dark"
          />
          <button
            type="submit"
            className="absolute right-2 top-1/2 -translate-y-1/2 text-brand-primary hover:text-action-hover hover:bg-action-light-5 transition-colors cursor-pointer bg-action-light-3 rounded-lg p-0.5"
          >
            <FiPlus size={20} />
          </button>
        </div>
      </form>
      {isCourseAdded && (
        <div className="flex flex-wrap gap-2 m-2">
          {" "}
          {coursesAddedList.map((course) => (
            <div
              key={course}
              className="flex bg-action-light-1 p-1 rounded-md gap-2 h-fit"
            >
              <div className=" text-text-badge text-xs font-semibold">
                {course}
              </div>
              <button className="cursor-pointer text-action-light-7 hover:text-action-light-5">
                <FiX size={15} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default CourseSelector;
