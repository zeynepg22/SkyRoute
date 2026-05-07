import { useEffect, useState } from "react"
import { Link, useParams } from "react-router-dom"
import Navbar from "../components/Navbar"
import { courseApi, lessonApi } from "../services/api"

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

export default function CourseDetail() {
  const { id } = useParams()

  const [course, setCourse] = useState(null)
  const [lessons, setLessons] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    async function fetchCourseDetail() {
      try {
        const courseData = await courseApi.getCourseById(id)
        const lessonData = await lessonApi.getLessonsByCourse(id)

        setCourse(courseData)
        setLessons(lessonData)
      } catch (err) {
        setError("Course details could not be loaded. Please check backend connection.")
      } finally {
        setLoading(false)
      }
    }

    fetchCourseDetail()
  }, [id])

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="min-h-screen bg-[#fff0f7] p-8">
          <p className="text-gray-500 text-lg">Loading course details...</p>
        </div>
      </>
    )
  }

  if (error || !course) {
    return (
      <>
        <Navbar />
        <div className="min-h-screen bg-[#fff0f7] p-8">
          <Link to="/courses" className="text-pink-500 font-bold">
            ← Back to Courses
          </Link>
          <p className="text-red-500 font-bold mt-8">
            {error || "Course not found."}
          </p>
        </div>
      </>
    )
  }

  const image = courseImages[(Number(id) - 1) % courseImages.length]

  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-[#fff0f7] p-8">
        <div className="max-w-6xl mx-auto">
          <Link
            to="/courses"
            className="text-pink-500 font-bold mb-8 inline-block"
          >
            ← Back to Courses
          </Link>

          <div className="grid lg:grid-cols-2 gap-10 items-center">
            <div>
              <span className="bg-pink-100 text-pink-500 px-4 py-2 rounded-full text-sm font-bold">
                {course.category || "Course"}
              </span>

              <h1 className="text-5xl font-extrabold mt-6 mb-5 leading-tight">
                {course.title}
              </h1>

              <p className="text-gray-600 text-lg leading-8 mb-8">
                {course.description ||
                  "Learn modern concepts with practical examples, interactive lessons, and real-world projects designed to improve your skills."}
              </p>

              <div className="flex flex-wrap items-center gap-6 mb-10">
                <span className="text-orange-400 font-bold text-lg">
                  ⭐ 4.8 Rating
                </span>

                <span className="text-gray-500">
                  Instructor: {course.instructor || "SkyRoute Instructor"}
                </span>

                <span className="text-gray-500">
                  Price: ${course.price || "49.99"}
                </span>
              </div>

              <div className="flex gap-4">
                <Link to={`/lesson/${course.id}`}>
                  <button className="bg-pink-500 text-white px-8 py-4 rounded-2xl font-bold hover:bg-pink-600 transition shadow-lg">
                    Start Lessons
                  </button>
                </Link>

                <button className="border border-pink-200 text-pink-500 px-8 py-4 rounded-2xl font-bold hover:bg-pink-50 transition">
                  Add Wishlist
                </button>
              </div>
            </div>

            <div className="bg-white rounded-[2rem] overflow-hidden shadow-2xl">
              <div className="h-[420px] overflow-hidden">
                <img
                  src={image}
                  alt={course.title}
                  className="w-full h-full object-cover"
                />
              </div>

              <div className="p-6">
                <h2 className="text-2xl font-extrabold mb-5">
                  Course Lessons
                </h2>

                <div className="space-y-4">
                  {lessons.length === 0 && (
                    <p className="text-gray-500">
                      No lessons found for this course.
                    </p>
                  )}

                  {lessons.map((lesson) => (
                    <Link
                      key={lesson.id}
                      to={`/lesson/${course.id}`}
                      className="flex items-center justify-between bg-pink-50 rounded-2xl p-5 hover:bg-pink-100 transition"
                    >
                      <span className="font-semibold">
                        {lesson.title}
                      </span>

                      <span className="text-pink-500 font-bold">
                        ▶
                      </span>
                    </Link>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}