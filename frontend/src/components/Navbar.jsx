import { Link } from "react-router-dom"

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between px-8 md:px-16 py-6 bg-[#fff7fb]">
      <Link to="/" className="flex items-center gap-3">
        <span className="text-4xl">🚀</span>

        <span className="font-extrabold text-4xl text-pink-500 tracking-tight">
          SkyRoute
        </span>
      </Link>

      <div className="hidden md:flex items-center gap-10 text-sm font-bold">
        <Link to="/" className="hover:text-pink-500 transition">
          Home
        </Link>

        <Link to="/courses" className="hover:text-pink-500 transition">
          Courses
        </Link>

        <Link to="/student/dashboard" className="hover:text-pink-500 transition">
          Student
        </Link>

        <Link to="/instructor/dashboard" className="hover:text-pink-500 transition">
          Instructor
        </Link>

        <Link to="/admin/dashboard" className="hover:text-pink-500 transition">
          Admin
        </Link>
      </div>

      <div className="flex items-center gap-4">
        <Link to="/login" className="font-semibold hover:text-pink-500 transition">
          Log in
        </Link>

        <Link
          to="/register"
          className="bg-pink-500 text-white px-6 py-3 rounded-2xl font-bold shadow-md hover:bg-pink-600 transition"
        >
          Sign up
        </Link>
      </div>
    </nav>
  )
}