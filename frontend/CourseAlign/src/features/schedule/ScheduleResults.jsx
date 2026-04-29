import {FiZap} from "react-icons/fi";

function ScheduleResults() {
  const isResults = true;
  return (
    <>
      <div className="mx-5 mb-5 mt-3">
        <button className="bg-brand-primary text-[15px] cursor-pointer hover:bg-action-hover transition-colors hover:text-text-secondary-light w-full p-3 rounded-lg flex items-center gap-3 justify-center font-semibold">
          <FiZap size={16} />
          Generate Results
        </button>
      </div>
      {isResults && (
        <div className="my-2">
          <p className="opacity-65 my-2 text-[13px] font-semibold uppercase">
            Results (3 found)
          </p>
          <div className="flex flex-col gap-2">
            <button className="flex w-full flex-col bg-action-light-1 rounded-lg p-2 gap-1 cursor-pointer hover:bg-action-light-3 transition-colors">
              <p className="text-left text-xs text-action-light-7 font-semibold ">
                Schedule 1
              </p>
              <div className="flex text-[11px] items-center gap-2 text-action-light-5">
                <p>No conflicts</p>
                <span>&mdash;</span>
                <p>3 courses</p>
              </div>
            </button>
            <button className="flex w-full flex-col bg-action-light-1 rounded-lg p-2 gap-1 cursor-pointer hover:bg-action-light-3 transition-colors">
              <p className="text-left text-xs text-action-light-7 font-semibold ">
                Schedule 1
              </p>
              <div className="flex text-[11px] items-center gap-2 text-action-light-5">
                <p>No conflicts</p>
                <span>&mdash;</span>
                <p>3 courses</p>
              </div>
            </button>
            <button className="flex w-full flex-col bg-action-light-1 rounded-lg p-2 gap-1 cursor-pointer hover:bg-action-light-3 transition-colors">
              <p className="text-left text-xs text-action-light-7 font-semibold ">
                Schedule 1
              </p>
              <div className="flex text-[11px] items-center gap-2 text-action-light-5">
                <p>No conflicts</p>
                <span>&mdash;</span>
                <p>3 courses</p>
              </div>
            </button>
            <button className="flex w-full flex-col bg-action-light-1 rounded-lg p-2 gap-1 cursor-pointer hover:bg-action-light-3 transition-colors">
              <p className="text-left text-xs text-action-light-7 font-semibold ">
                Schedule 1
              </p>
              <div className="flex text-[11px] items-center gap-2 text-action-light-5">
                <p>No conflicts</p>
                <span>&mdash;</span>
                <p>3 courses</p>
              </div>
            </button>
          </div>
        </div>
      )}
    </>
  );
}

export default ScheduleResults;
