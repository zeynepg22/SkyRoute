import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import Navbar from "../components/Navbar"
import { courseApi } from "../services/api"

import reactCourse from "../assets/react-course.png"
import pythonCourse from "../assets/python-course.png"
import designCourse from "../assets/design-course.png"
import marketingCourse from "../assets/marketing-course.png"
import businessCourse from "../assets/business-course.png"
import growthCourse from "../assets/growth-course.png"

const courseImages = [
  reactCourse,
  pythonCourse,
  designCourse,
  marketingCourse,
  businessCourse,
  growthCourse,
]

export default function Courses() {
  const [courses, setCourses] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    async function fetchCourses() {
      try {
        const data = await courseApi.getCourses()
        setCourses(data)
      } catch (err) {
        setError("Courses could not be loaded. Please check backend connection.")
      } finally {
        setLoading(false)
      }
    }

    fetchCourses()
  }, [])

  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-[#fff0f7] p-8">
        <div className="max-w-[1700px] mx-auto">
          <h1 className="text-5xl font-extrabold mb-3">
            All Courses
          </h1>

          <p className="text-gray-500 text-lg mb-10">
            Browse available courses and choose your learning path.
          </p>

          {loading && (
            <p className="text-gray-500 text-lg">
              Loading courses...
            </p>
          )}

          {error && (
            <p className="text-red-500 font-bold">
              {error}
            </p>
          )}

          {!loading && !error && (
            <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-8">
              {courses.map((course, index) => (
                <div
                  key={course.id}
                  className="bg-white rounded-[2rem] overflow-hidden shadow-lg hover:shadow-2xl transition duration-300 hover:-translate-y-2"
                >
                  <div className="h-64 overflow-hidden relative">
                    {index < 2 && (
                      <div className="absolute top-4 left-4 z-20 bg-yellow-400 text-black text-xs font-extrabold px-4 py-2 rounded-full shadow-lg">
                        🔥 BEST SELLER
                      </div>
                    )}

                    <img
                      src={courseImages[index % courseImages.length]}
                      alt={course.title}
                      className="w-full h-full object-cover"
                    />
                  </div>

                  <div className="p-6">
                    <span className="text-xs font-bold text-pink-500 bg-pink-50 px-4 py-2 rounded-full">
                      {course.category || "Course"}
                    </span>

                    <h2 className="text-2xl font-extrabold mt-5 mb-3 leading-snug">
                      {course.title}
                    </h2>

                    <p className="text-gray-500 mb-6">
                      Instructor: {course.instructor || "SkyRoute Instructor"}
                    </p>

                    <div className="flex items-center justify-between mb-6">
                      <span className="text-orange-400 font-bold text-lg">
                        ⭐ 4.8
                      </span>

                      <span className="font-extrabold text-2xl">
                        ${course.price || "49.99"}
                      </span>
                    </div>

                    <Link to={`/courses/${course.id}`}>
                      <button className="w-full bg-pink-500 text-white py-4 rounded-2xl font-extrabold text-lg hover:bg-pink-600 transition shadow-md">
                        Enroll Now
                      </button>
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  )
}