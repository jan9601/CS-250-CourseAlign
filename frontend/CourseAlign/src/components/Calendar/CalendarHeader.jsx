import {FiCalendar} from "react-icons/fi";

function CalendarHeader() {
  return (
    <div className="flex items-center justify-between p-4 border-b border-border">
      <div className="flex items-center gap-2 text-text-primary-light">
        <FiCalendar size={18} className="text-brand-primary" />
        <span className="font-medium">Schedule 1</span>
      </div>
      <span className="text-xs text-text-secondary-light opacity-60">
        3 courses · No conflicts
      </span>
    </div>
  );
}

export default CalendarHeader;
