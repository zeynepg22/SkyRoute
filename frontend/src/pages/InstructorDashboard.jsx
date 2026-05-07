import Navbar from "../components/Navbar"

export default function InstructorDashboard() {
  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-[#fff7fb] p-8">
        <h1 className="text-4xl font-extrabold mb-2">
          Instructor Dashboard 👨‍🏫
        </h1>

        <p className="text-gray-500 mb-8">
          Manage your courses and monitor student engagement.
        </p>

        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-3xl p-6 shadow-md">
            <h2 className="text-gray-500 mb-2">
              Published Courses
            </h2>

            <p className="text-4xl font-extrabold text-pink-500">
              8
            </p>
          </div>

          <div className="bg-white rounded-3xl p-6 shadow-md">
            <h2 className="text-gray-500 mb-2">
              Total Students
            </h2>

            <p className="text-4xl font-extrabold text-pink-500">
              1,240
            </p>
          </div>

          <div className="bg-white rounded-3xl p-6 shadow-md">
            <h2 className="text-gray-500 mb-2">
              Monthly Revenue
            </h2>

            <p className="text-4xl font-extrabold text-pink-500">
              $4.8K
            </p>
          </div>
        </div>

        <div className="bg-white rounded-3xl shadow-md p-6">
          <h2 className="text-2xl font-bold mb-6">
            Your Top Courses
          </h2>

          <div className="space-y-5">
            {[
              ["React Masterclass", "4.9 ⭐"],
              ["Advanced UI/UX", "4.8 ⭐"],
              ["Python Bootcamp", "4.7 ⭐"],
            ].map((course, index) => (
              <div
                key={index}
                className="flex justify-between items-center bg-pink-50 rounded-2xl p-4"
              >
                <span className="font-semibold">
                  {course[0]}
                </span>

                <span className="text-pink-500 font-bold">
                  {course[1]}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  )
}