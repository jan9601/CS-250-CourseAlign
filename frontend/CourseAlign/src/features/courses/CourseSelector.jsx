import Input from "../../components/ui/Input";

function CourseSelector() {
  return (
    <div className="p-2">
      <p className="opacity-65 my-2">Courses</p>
      <Input placeholder="Search course... (CS 250)" />
      <div className="border-b border-border mt-4" />
    </div>
  );
}

export default CourseSelector;
