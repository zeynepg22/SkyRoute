import Navbar from "../components/Navbar"

export default function AdminDashboard() {
  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-[#fff7fb] p-8">
        <h1 className="text-4xl font-extrabold mb-2">
          Admin Dashboard 🛠️
        </h1>

        <p className="text-gray-500 mb-8">
          Monitor platform statistics and manage the system.
        </p>

        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-3xl p-6 shadow-md">
            <h2 className="text-gray-500 mb-2">Users</h2>

            <p className="text-4xl font-extrabold text-pink-500">
              15K
            </p>
          </div>

          <div className="bg-white rounded-3xl p-6 shadow-md">
            <h2 className="text-gray-500 mb-2">Courses</h2>

            <p className="text-4xl font-extrabold text-pink-500">
              520
            </p>
          </div>

          <div className="bg-white rounded-3xl p-6 shadow-md">
            <h2 className="text-gray-500 mb-2">
              Instructors
            </h2>

            <p className="text-4xl font-extrabold text-pink-500">
              120
            </p>
          </div>

          <div className="bg-white rounded-3xl p-6 shadow-md">
            <h2 className="text-gray-500 mb-2">Revenue</h2>

            <p className="text-4xl font-extrabold text-pink-500">
              $24K
            </p>
          </div>
        </div>

        <div className="bg-white rounded-3xl shadow-md p-6">
          <h2 className="text-2xl font-bold mb-6">
            Recent Activities
          </h2>

          <div className="space-y-4">
            {[
              "New instructor registered",
              "React course updated",
              "120 new students joined",
              "Payment successfully processed",
            ].map((activity, index) => (
              <div
                key={index}
                className="bg-pink-50 rounded-2xl p-4 font-medium"
              >
                {activity}
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  )
}