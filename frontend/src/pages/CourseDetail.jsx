import { Link, useParams } from "react-router-dom"
import Navbar from "../components/Navbar"

import reactCourse from "../assets/react-course.png"
import pythonCourse from "../assets/python-course.png"
import designCourse from "../assets/design-course.png"
import marketingCourse from "../assets/marketing-course.png"
import businessCourse from "../assets/business-course.png"
import growthCourse from "../assets/growth-course.png"

export default function CourseDetail() {
  const { id } = useParams()

  const courses = {
    1: {
      title: "React JS Complete Masterclass",
      category: "Development",
      instructor: "John Doe",
      image: reactCourse,
    },
    2: {
      title: "Python for Data Science",
      category: "Data Science",
      instructor: "Jane Smith",
      image: pythonCourse,
    },
    3: {
      title: "UI/UX Design Fundamentals",
      category: "Design",
      instructor: "Alex Johnson",
      image: designCourse,
    },
    4: {
      title: "Digital Marketing Masterclass",
      category: "Marketing",
      instructor: "Sarah Lee",
      image: marketingCourse,
    },
    5: {
      title: "Business Strategy Basics",
      category: "Business",
      instructor: "Mike Brown",
      image: businessCourse,
    },
    6: {
      title: "Personal Growth Bootcamp",
      category: "Growth",
      instructor: "Emma Wilson",
      image: growthCourse,
    },
  }

  const course = courses[id] || courses[1]

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
                {course.category}
              </span>

              <h1 className="text-5xl font-extrabold mt-6 mb-5 leading-tight">
                {course.title}
              </h1>

              <p className="text-gray-600 text-lg leading-8 mb-8">
                Learn modern concepts with practical examples, interactive
                lessons, and real-world projects designed to improve your skills.
              </p>

              <div className="flex flex-wrap items-center gap-6 mb-10">
                <span className="text-orange-400 font-bold text-lg">
                  ⭐ 4.8 Rating
                </span>

                <span className="text-gray-500">
                  12,540 Students
                </span>

                <span className="text-gray-500">
                  Instructor: {course.instructor}
                </span>
              </div>

              <div className="flex gap-4">
                <Link to={`/lesson/${id}`}>
                  <button className="bg-pink-500 text-white px-8 py-4 rounded-2xl font-bold hover:bg-pink-600 transition shadow-lg">
                    Enroll Now
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
                  src={course.image}
                  alt={course.title}
                  className="w-full h-full object-cover"
                />
              </div>

              <div className="p-6">
                <h2 className="text-2xl font-extrabold mb-5">
                  Course Lessons
                </h2>

                <div className="space-y-4">
                  {[
                    "Introduction",
                    "Core Concepts",
                    "Advanced Techniques",
                    "Projects",
                    "Final Review",
                  ].map((lesson, index) => (
                    <Link
                      key={index}
                      to={`/lesson/${id}`}
                      className="flex items-center justify-between bg-pink-50 rounded-2xl p-5 hover:bg-pink-100 transition"
                    >
                      <span className="font-semibold">
                        {lesson}
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