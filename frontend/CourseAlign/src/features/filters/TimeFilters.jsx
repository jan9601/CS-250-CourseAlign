import Input from "../../components/ui/Input";

function TimeFilters() {
  return (
    <div className="p-2">
      <p className="opacity-65 my-2">Time Preferences</p>
      <div className="flex gap-6 items-center">
        <p className="opacity-50 text-[10px]">Earliest Start</p>
        <p className="opacity-50 text-[10px]">Latest end</p>
      </div>
      <div className="border-border border-b mt-4" />
    </div>
  );
}

export default TimeFilters;
