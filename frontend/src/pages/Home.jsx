import Navbar from "../components/Navbar"
import heroStudent from "../assets/hero-student.png"

export default function Home() {
  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-[#fff7fb] text-[#2b2b35] overflow-hidden">
        <section className="grid lg:grid-cols-2 gap-6 items-center px-8 md:px-16 py-12">

          <div>
            <p className="text-pink-500 font-semibold mb-4">
              Learn. Grow. Succeed.
            </p>

            <h1 className="text-5xl md:text-7xl font-extrabold leading-tight mb-6">
              Your Journey to <br />
              <span className="text-pink-500">New Skills</span> <br />
              Starts Here.
            </h1>

            <p className="text-gray-600 max-w-xl mb-8 text-lg leading-8">
              Discover expert-led online courses, enroll easily, watch lessons,
              and track your learning progress with a modern course platform.
            </p>

            <div className="flex gap-4 mb-12">
              <button className="bg-pink-500 text-white px-8 py-4 rounded-2xl font-bold shadow-lg hover:bg-pink-600 transition">
                Browse Courses
              </button>

              <button className="border border-pink-200 text-pink-500 px-8 py-4 rounded-2xl font-bold hover:bg-pink-50 transition">
                Become Instructor
              </button>
            </div>

            <div className="bg-white rounded-[2rem] shadow-xl p-6 flex flex-wrap gap-10 max-w-xl border border-pink-50">
              <div className="flex items-center gap-3">
                <div className="bg-pink-100 text-pink-500 w-14 h-14 rounded-full flex items-center justify-center text-2xl">
                  👥
                </div>

                <div>
                  <h3 className="font-extrabold text-3xl">
                    12K+
                  </h3>

                  <p className="text-gray-500 text-sm">
                    Students
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <div className="bg-purple-100 text-purple-500 w-14 h-14 rounded-full flex items-center justify-center text-2xl">
                  📚
                </div>

                <div>
                  <h3 className="font-extrabold text-3xl">
                    500+
                  </h3>

                  <p className="text-gray-500 text-sm">
                    Courses
                  </p>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <div className="bg-yellow-100 text-yellow-500 w-14 h-14 rounded-full flex items-center justify-center text-2xl">
                  ⭐
                </div>

                <div>
                  <h3 className="font-extrabold text-3xl">
                    4.9
                  </h3>

                  <p className="text-gray-500 text-sm">
                    Rating
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="relative flex items-center justify-center">

            <div className="absolute w-[760px] h-[760px] rounded-full bg-gradient-to-br from-pink-100 via-pink-50 to-[#fff7fb] blur-3xl opacity-90"></div>

            <img
              src={heroStudent}
              alt="Online Learning"
              className="relative z-10 w-full max-w-[900px] object-contain scale-110"
            />
          </div>

        </section>

        <section className="px-8 md:px-16 pb-16">
          <div className="bg-white rounded-[2.5rem] shadow-xl p-12 text-center border border-pink-50">

            <p className="text-gray-500 font-semibold mb-10 text-lg">
              Trusted by thousands of learners and organizations
            </p>

            <div className="grid grid-cols-2 md:grid-cols-5 gap-10 text-3xl font-extrabold text-gray-400">
              <span>Google</span>
              <span>Microsoft</span>
              <span>Stripe</span>
              <span>Amazon</span>
              <span>Udemy</span>
            </div>

          </div>
        </section>
      </div>
    </>
  )
}