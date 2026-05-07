import { Link, useParams } from "react-router-dom"
import Navbar from "../components/Navbar"

export default function LessonPage() {
  const { id } = useParams()

  const lessons = {
    1: {
      title: "React Introduction Lesson",
      description:
        "Learn the fundamentals of React, JSX, components, hooks, and modern frontend development.",
      video: "https://www.youtube.com/embed/SqcY0GlETPk",
      duration: "12 min",
      course: "React Masterclass",
    },

    2: {
      title: "Python for Data Science",
      description:
        "Explore Python fundamentals, data analysis, machine learning basics, and real-world datasets.",
      video: "https://www.youtube.com/embed/LHBE6Q9XlzI",
      duration: "18 min",
      course: "Python Bootcamp",
    },

    3: {
      title: "UI/UX Design Fundamentals",
      description:
        "Understand user experience, interface design principles, wireframing, and visual hierarchy.",
      video: "https://www.youtube.com/embed/c9Wg6Cb_YlU",
      duration: "20 min",
      course: "UI/UX Design",
    },

    4: {
      title: "Digital Marketing Basics",
      description:
        "Learn SEO, social media strategy, branding, audience targeting, and marketing campaigns.",
      video: "https://www.youtube.com/embed/JghrmfcukOs",
      duration: "16 min",
      course: "Marketing Masterclass",
    },

    5: {
      title: "Business Strategy Essentials",
      description:
        "Master strategic planning, leadership, competitive analysis, and business growth techniques.",
      video: "https://www.youtube.com/embed/o7Ik1OB4TaE",
      duration: "14 min",
      course: "Business Strategy",
    },

    6: {
      title: "Personal Growth & Productivity",
      description:
        "Improve focus, discipline, productivity habits, mindset, and personal development skills.",
      video: "https://www.youtube.com/embed/Lp7E973zozc",
      duration: "15 min",
      course: "Growth Bootcamp",
    },
  }

  const lesson = lessons[id] || lessons[1]

  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-[#fff0f7] p-8">
        <div className="max-w-7xl mx-auto">
          <Link
            to={`/courses/${id}`}
            className="text-pink-500 font-bold mb-8 inline-block"
          >
            ← Back to Course
          </Link>

          <div className="grid lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <div className="bg-white rounded-[2rem] shadow-2xl overflow-hidden">
                <div className="aspect-video">
                  <iframe
                    className="w-full h-full"
                    src={lesson.video}
                    title={lesson.title}
                    allowFullScreen
                  ></iframe>
                </div>

                <div className="p-8">
                  <span className="bg-pink-100 text-pink-500 px-4 py-2 rounded-full text-sm font-bold">
                    {lesson.course}
                  </span>

                  <h1 className="text-4xl font-extrabold mt-5 mb-4 leading-tight">
                    {lesson.title}
                  </h1>

                  <p className="text-gray-600 text-lg leading-8 mb-8">
                    {lesson.description}
                  </p>

                  <div className="flex items-center gap-6 mb-8">
                    <span className="text-orange-400 font-bold">
                      ⭐ 4.8 Rating
                    </span>

                    <span className="text-gray-500">
                      Duration: {lesson.duration}
                    </span>

                    <span className="text-gray-500">
                      12K+ Students
                    </span>
                  </div>

                  <button className="bg-pink-500 text-white px-8 py-4 rounded-2xl font-bold hover:bg-pink-600 transition shadow-lg">
                    Mark as Complete
                  </button>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-[2rem] shadow-2xl p-6 h-fit">
              <h2 className="text-2xl font-extrabold mb-6">
                Course Content
              </h2>

              <div className="space-y-4">
                {Object.entries(lessons).map(([lessonId, item]) => (
                  <Link
                    key={lessonId}
                    to={`/lesson/${lessonId}`}
                    className={`flex items-center justify-between rounded-2xl p-5 transition ${
                      lessonId == id
                        ? "bg-pink-500 text-white"
                        : "bg-pink-50 hover:bg-pink-100"
                    }`}
                  >
                    <div>
                      <p className="font-semibold">
                        {item.title}
                      </p>

                      <p
                        className={`text-sm ${
                          lessonId == id
                            ? "text-pink-100"
                            : "text-gray-500"
                        }`}
                      >
                        {item.duration}
                      </p>
                    </div>

                    <span className="font-bold">▶</span>
                  </Link>
                ))}
              </div>

              <div className="mt-10">
                <div className="flex justify-between mb-3">
                  <span className="font-semibold">
                    Course Progress
                  </span>

                  <span className="text-pink-500 font-bold">
                    60%
                  </span>
                </div>

                <div className="w-full h-4 bg-pink-100 rounded-full overflow-hidden">
                  <div className="h-4 bg-pink-500 rounded-full w-[60%]"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}