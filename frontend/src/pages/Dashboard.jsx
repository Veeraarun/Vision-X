import DashboardLayout from "../layouts/DashboardLayout";
import StatCard from "../components/StatCard";

export default function Dashboard() {
  return (
    <DashboardLayout>

      <div className="grid grid-cols-4 gap-6">

        <StatCard
          title="Patients"
          value="32"
        />

        <StatCard
          title="Today's Sessions"
          value="8"
        />

        <StatCard
          title="Completed"
          value="21"
        />

        <StatCard
          title="Average Stress"
          value="18%"
        />

      </div>

    </DashboardLayout>
  );
}