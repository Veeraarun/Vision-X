export default function StatCard({
  title,
  value,
}) {
  return (
    <div className="bg-white rounded-2xl shadow-md p-6">

      <h3 className="text-gray-500">
        {title}
      </h3>

      <p className="text-3xl font-bold mt-3">
        {value}
      </p>

    </div>
  );
}