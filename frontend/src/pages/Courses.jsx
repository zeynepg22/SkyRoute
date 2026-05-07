import { Link } from "react-router-dom"
import Navbar from "../components/Navbar"

import reactCourse from "../assets/react-course.png"
import pythonCourse from "../assets/python-course.png"
import designCourse from "../assets/design-course.png"
import marketingCourse from "../assets/marketing-course.png"
import businessCourse from "../assets/business-course.png"
import growthCourse from "../assets/growth-course.png"

export default function Courses() {
  const courses = [
    [
      "React JS - Complete Guide",
      "John Doe",
      "Development",
      "$49.99",
      reactCourse,
      true,
    ],

    [
      "Python for Data Science",
      "Jane Smith",
      "Data Science",
      "$44.99",
      pythonCourse,
      true,
    ],

    [
      "UI/UX Design Fundamentals",
      "Alex Johnson",
      "Design",
      "$39.99",
      designCourse,
      false,
    ],

    [
      "Digital Marketing Masterclass",
      "Sarah Lee",
      "Marketing",
      "$34.99",
      marketingCourse,
      true,
    ],

    [
      "Business Strategy Basics",
      "Mike Brown",
      "Business",
      "$29.99",
      businessCourse,
      false,
    ],

    [
      "Personal Growth Bootcamp",
      "Emma Wilson",
      "Growth",
      "$24.99",
      growthCourse,
      false,
    ],
  ]

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

          <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-8">

            {courses.map((course, index) => (
              <div
                key={index}
                className="bg-white rounded-[2rem] overflow-hidden shadow-lg hover:shadow-2xl transition duration-300 hover:-translate-y-2"
              >

                <div className="h-64 overflow-hidden relative">

                  {course[5] && (
                    <div className="absolute top-4 left-4 z-20 bg-yellow-400 text-black text-xs font-extrabold px-4 py-2 rounded-full shadow-lg">
                      🔥 BEST SELLER
                    </div>
                  )}

                  <img
                    src={course[4]}
                    alt={course[0]}
                    className="w-full h-full object-cover"
                  />
                </div>

                <div className="p-6">

                  <span className="text-xs font-bold text-pink-500 bg-pink-50 px-4 py-2 rounded-full">
                    {course[2]}
                  </span>

                  <h2 className="text-2xl font-extrabold mt-5 mb-3 leading-snug">
                    {course[0]}
                  </h2>

                  <p className="text-gray-500 mb-6">
                    Instructor: {course[1]}
                  </p>

                  <div className="flex items-center justify-between mb-6">

                    <span className="text-orange-400 font-bold text-lg">
                      ⭐ 4.8
                    </span>

                    <span className="font-extrabold text-2xl">
                      {course[3]}
                    </span>

                  </div>

                  <Link to={`/courses/${index + 1}`}>
                    <button className="w-full bg-pink-500 text-white py-4 rounded-2xl font-extrabold text-lg hover:bg-pink-600 transition shadow-md">
                      Enroll Now
                    </button>
                  </Link>

                </div>
              </div>
            ))}

          </div>
        </div>
      </div>
    </>
  )
}