import { Link } from "react-router-dom"
import Navbar from "../components/Navbar"

export default function Register() {
  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-[#fef7fb] flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-6xl bg-white rounded-[2.5rem] overflow-hidden shadow-2xl grid lg:grid-cols-2">
          <div className="p-10 md:p-16 flex flex-col justify-center">
            <h2 className="text-pink-500 font-extrabold text-2xl mb-3">
              🚀 SkyRoute
            </h2>

            <h1 className="text-4xl font-extrabold mb-3">
              Create your account
            </h1>

            <p className="text-gray-500 mb-8">
              Join the platform and start learning with expert-led courses.
            </p>

            <form className="space-y-5">
              <div>
                <label className="block text-sm font-bold mb-2">
                  Full Name
                </label>
                <input
                  type="text"
                  placeholder="Alex Johnson"
                  className="w-full border border-pink-100 rounded-2xl px-5 py-4 outline-none focus:border-pink-400 transition"
                />
              </div>

              <div>
                <label className="block text-sm font-bold mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  placeholder="alex@example.com"
                  className="w-full border border-pink-100 rounded-2xl px-5 py-4 outline-none focus:border-pink-400 transition"
                />
              </div>

              <div>
                <label className="block text-sm font-bold mb-2">
                  Password
                </label>
                <input
                  type="password"
                  placeholder="••••••••"
                  className="w-full border border-pink-100 rounded-2xl px-5 py-4 outline-none focus:border-pink-400 transition"
                />
              </div>

              <div>
                <label className="block text-sm font-bold mb-2">
                  Confirm Password
                </label>
                <input
                  type="password"
                  placeholder="••••••••"
                  className="w-full border border-pink-100 rounded-2xl px-5 py-4 outline-none focus:border-pink-400 transition"
                />
              </div>

              <div>
                <label className="block text-sm font-bold mb-2">
                  Account Type
                </label>
                <select className="w-full border border-pink-100 rounded-2xl px-5 py-4 outline-none focus:border-pink-400 transition bg-white">
                  <option>Student</option>
                  <option>Instructor</option>
                </select>
              </div>

              <button
                type="submit"
                className="w-full bg-pink-500 text-white py-4 rounded-2xl font-extrabold shadow-lg hover:bg-pink-600 transition"
              >
                Create Account
              </button>
            </form>

            <div className="flex items-center gap-4 my-7">
              <div className="flex-1 h-[1px] bg-gray-200"></div>
              <span className="text-gray-400 text-sm">or sign up with</span>
              <div className="flex-1 h-[1px] bg-gray-200"></div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <button className="border border-pink-100 rounded-2xl py-4 font-bold hover:bg-pink-50 transition">
                Google
              </button>

              <button className="border border-pink-100 rounded-2xl py-4 font-bold hover:bg-pink-50 transition">
                GitHub
              </button>
            </div>

            <p className="text-center text-gray-500 mt-8">
              Already have an account?{" "}
              <Link to="/login" className="text-pink-500 font-bold">
                Log in
              </Link>
            </p>
          </div>

          <div className="hidden lg:flex bg-gradient-to-br from-[#ffb6d9] to-[#ff5ca8] items-center justify-center relative overflow-hidden">
            <div className="absolute inset-0 bg-white/10 backdrop-blur-sm"></div>

            <div className="relative z-10 flex flex-col items-center text-center px-10">
              <img
                src="/hero-girl.png"
                alt="Register Illustration"
                className="w-[430px] object-contain drop-shadow-2xl"
              />

              <h1 className="text-5xl font-extrabold text-white mt-6 mb-4">
                Start Learning Today
              </h1>

              <p className="text-white/90 text-lg leading-8 max-w-md">
                Create your profile, enroll in courses, and monitor your
                progress from your personal dashboard.
              </p>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}