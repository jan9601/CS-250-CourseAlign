import {useState} from "react";
import AppLayout from "./components/layout/AppLayout";

function App() {
  const [courses, setCourses] = useState([]);
  const [earliestStart, setEarliestStart] = useState("08:00");
  const [latestEnd, setLatestEnd] = useState("22:00");

  return (
    <div>
      <AppLayout
        courses={courses}
        setCourses={setCourses}
        earliestStart={earliestStart}
        setEarliestStart={setEarliestStart}
        latestEnd={latestEnd}
        setLatestEnd={setLatestEnd}
      />
    </div>
  );
}

export default App;
