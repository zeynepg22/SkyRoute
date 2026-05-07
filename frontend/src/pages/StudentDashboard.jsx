import Navbar from "../components/Navbar"

export default function StudentDashboard() {
  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-[#fff7fb] p-8">
        <h1 className="text-4xl font-extrabold mb-2">
          Student Dashboard 🎓
        </h1>

        <p className="text-gray-500 mb-8">
          Track your enrolled courses and learning progress.
        </p>

        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-3xl p-6 shadow-md">
            <h2 className="text-gray-500 mb-2">Enrolled Courses</h2>
            <p className="text-4xl font-extrabold text-pink-500">12</p>
          </div>

          <div className="bg-white rounded-3xl p-6 shadow-md">
            <h2 className="text-gray-500 mb-2">Completed Lessons</h2>
            <p className="text-4xl font-extrabold text-pink-500">48</p>
          </div>

          <div className="bg-white rounded-3xl p-6 shadow-md">
            <h2 className="text-gray-500 mb-2">Certificates</h2>
            <p className="text-4xl font-extrabold text-pink-500">5</p>
          </div>
        </div>

        <div className="bg-white rounded-3xl shadow-md p-6">
          <h2 className="text-2xl font-bold mb-6">Continue Learning</h2>

          <div className="space-y-5">
            {[
              ["React Development", "75%"],
              ["UI/UX Design", "40%"],
              ["Python Fundamentals", "90%"],
            ].map((course, index) => (
              <div key={index}>
                <div className="flex justify-between mb-2">
                  <span className="font-semibold">{course[0]}</span>
                  <span className="text-pink-500 font-bold">{course[1]}</span>
                </div>

                <div className="w-full h-3 bg-pink-100 rounded-full">
                  <div
                    className="h-3 bg-pink-500 rounded-full"
                    style={{ width: course[1] }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  )
}