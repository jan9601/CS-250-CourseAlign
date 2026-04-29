const timeOptions = [
  {label: "8:00 AM", value: "08:00"},
  {label: "9:00 AM", value: "09:00"},
  {label: "10:00 AM", value: "10:00"},
  {label: "11:00 AM", value: "11:00"},
  {label: "12:00 PM", value: "12:00"},
  {label: "1:00 PM", value: "13:00"},
  {label: "2:00 PM", value: "14:00"},
  {label: "3:00 PM", value: "15:00"},
  {label: "4:00 PM", value: "16:00"},
  {label: "5:00 PM", value: "17:00"},
  {label: "6:00 PM", value: "18:00"},
  {label: "7:00 PM", value: "19:00"},
  {label: "8:00 PM", value: "20:00"},
  {label: "9:00 PM", value: "21:00"},
  {label: "10:00 PM", value: "22:00"},
];
function TimeFilters() {
  return (
    <div className="mt-3 mb-5">
      <p className="opacity-65 mb-3 text-[14px] uppercase font-semibold">
        Time Preferences
      </p>
      <div className="flex flex-col gap-2">
        <div className="flex items-center gap-1">
          <span className="opacity-50 text-sm">Earliest Start:</span>
          <select className="bg-brand-dark-1 rounded-sm cursor-pointer text-xs">
            {timeOptions.map((option) => (
              <option
                className="text-text-primary-light"
                key={option.value}
                value={option.value}
              >
                {option.label}
              </option>
            ))}
          </select>
        </div>
        <div className="flex items-center gap-1">
          <span className="opacity-50 text-sm">Latest end:</span>
          <select className="bg-brand-dark-1 rounded-sm cursor-pointer text-xs">
            {timeOptions.map((option) => (
              <option
                className="text-text-primary-light"
                key={option.value}
                value={option.value}
              >
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
}

export default TimeFilters;
