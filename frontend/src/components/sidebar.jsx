const menu = [
  "Dashboard",
  "Patients",
  "AI Clinical Assistant",
  "Live Session",
  "Reports",
  "Settings",
];

export default function Sidebar() {
  return (
    <aside className="w-72 bg-white shadow-md">

      <div className="p-8 border-b">

        <h1 className="text-3xl font-bold text-blue-600">
          Vision-X
        </h1>

        <p className="text-gray-500 text-sm mt-2">
          AI Co-Therapist
        </p>

      </div>

      <nav className="p-4">

        {menu.map((item) => (

          <button
            key={item}
            className="w-full text-left px-5 py-4 rounded-xl hover:bg-blue-50 mb-2 transition"
          >
            {item}
          </button>

        ))}

      </nav>

    </aside>
  );
}