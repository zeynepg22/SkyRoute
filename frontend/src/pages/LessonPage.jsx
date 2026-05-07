import { useEffect, useState } from "react"
import { Link, useParams } from "react-router-dom"
import Navbar from "../components/Navbar"
import { lessonApi, progressApi } from "../services/api"

const courseVideos = {
  1: "https://www.youtube.com/embed/SqcY0GlETPk",
  2: "https://www.youtube.com/embed/LHBE6Q9XlzI",
  3: "https://www.youtube.com/embed/c9Wg6Cb_YlU",
  4: "https://www.youtube.com/embed/nU-IIXBWlS4",
  5: "https://www.youtube.com/embed/o7Ik1OB4TaE",
  6: "https://www.youtube.com/embed/ZXsQAXx_ao0",
}

export default function LessonPage() {
  const { id } = useParams()

  const [lesson, setLesson] = useState(null)
  const [courseLessons, setCourseLessons] = useState([])
  const [progress, setProgress] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [successMessage, setSuccessMessage] = useState("")

  useEffect(() => {
    async function fetchLessonData() {
      try {
        setLoading(true)

        const courseId = id
        const lessons = await lessonApi.getLessonsByCourse(courseId)

        setCourseLessons(lessons)

        if (lessons.length > 0) {
          setLesson(lessons[0])
        } else {
          setLesson(null)
        }

        const progressData = await progressApi.getProgress(courseId)
        setProgress(progressData.progress || 0)
      } catch (err) {
        setError("Lesson could not be loaded. Please check backend connection.")
      } finally {
        setLoading(false)
      }
    }

    fetchLessonData()
  }, [id])

  async function handleCompleteLesson() {
    try {
      if (!lesson) return

      await progressApi.completeLesson(lesson.id)
      setSuccessMessage("Lesson marked as complete.")

      const progressData = await progressApi.getProgress(id)
      setProgress(progressData.progress || 0)
    } catch (err) {
      setError("Lesson could not be completed.")
    }
  }

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="min-h-screen bg-[#fff0f7] p-8">
          <p className="text-gray-500 text-lg">Loading lesson...</p>
        </div>
      </>
    )
  }

  if (error || !lesson) {
    return (
      <>
        <Navbar />
        <div className="min-h-screen bg-[#fff0f7] p-8">
          <Link to="/courses" className="text-pink-500 font-bold">
            ← Back to Courses
          </Link>

          <p className="text-red-500 font-bold mt-8">
            {error || "Lesson not found."}
          </p>
        </div>
      </>
    )
  }

  const video = courseVideos[id] || "https://www.youtube.com/embed/SqcY0GlETPk"

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
                    src={video}
                    title={lesson.title}
                    allowFullScreen
                  ></iframe>
                </div>

                <div className="p-8">
                  <span className="bg-pink-100 text-pink-500 px-4 py-2 rounded-full text-sm font-bold">
                    Course ID: {id}
                  </span>

                  <h1 className="text-4xl font-extrabold mt-5 mb-4 leading-tight">
                    {lesson.title}
                  </h1>

                  <p className="text-gray-600 text-lg leading-8 mb-8">
                    {lesson.content ||
                      lesson.description ||
                      "This lesson introduces the main concepts with practical examples."}
                  </p>

                  <div className="flex items-center gap-6 mb-8">
                    <span className="text-orange-400 font-bold">
                      ⭐ 4.8 Rating
                    </span>

                    <span className="text-gray-500">
                      Duration: {lesson.duration || "15 min"}
                    </span>

                    <span className="text-gray-500">
                      12K+ Students
                    </span>
                  </div>

                  {successMessage && (
                    <p className="text-green-600 font-bold mb-5">
                      {successMessage}
                    </p>
                  )}

                  <button
                    onClick={handleCompleteLesson}
                    className="bg-pink-500 text-white px-8 py-4 rounded-2xl font-bold hover:bg-pink-600 transition shadow-lg"
                  >
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
                {courseLessons.map((item) => (
                  <button
                    key={item.id}
                    onClick={() => {
                      setLesson(item)
                      setSuccessMessage("")
                    }}
                    className={`w-full text-left flex items-center justify-between rounded-2xl p-5 transition ${
                      item.id === lesson.id
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
                          item.id === lesson.id
                            ? "text-pink-100"
                            : "text-gray-500"
                        }`}
                      >
                        {item.duration || "15 min"}
                      </p>
                    </div>

                    <span className="font-bold">▶</span>
                  </button>
                ))}
              </div>

              <div className="mt-10">
                <div className="flex justify-between mb-3">
                  <span className="font-semibold">
                    Course Progress
                  </span>

                  <span className="text-pink-500 font-bold">
                    {progress}%
                  </span>
                </div>

                <div className="w-full h-4 bg-pink-100 rounded-full overflow-hidden">
                  <div
                    className="h-4 bg-pink-500 rounded-full"
                    style={{ width: `${progress}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}