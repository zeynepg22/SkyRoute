import Navbar from "../components/Navbar"

export default function Login() {
  return (
    <>
      <Navbar />

      <div className="min-h-screen bg-[#fef7fb] flex items-center justify-center px-6 py-12">

        <div className="w-full max-w-6xl bg-white rounded-[2.5rem] overflow-hidden shadow-2xl grid lg:grid-cols-2">

          {/* LEFT SIDE */}

          <div className="hidden lg:flex bg-gradient-to-br from-[#ffb6d9] to-[#ff5ca8] items-center justify-center relative overflow-hidden">

            <div className="absolute inset-0 bg-white/10 backdrop-blur-sm"></div>

            <div className="relative z-10 flex flex-col items-center text-center px-10">

              <img
                src="/login-boy.png"
                alt="Login Illustration"
                className="w-[420px] object-contain drop-shadow-2xl"
              />

              <h1 className="text-5xl font-extrabold text-white mt-6 mb-4">
                Welcome Back!
              </h1>

              <p className="text-white/90 text-lg leading-8 max-w-md">
                Continue your learning journey and track your course progress.
              </p>

            </div>
          </div>

          {/* RIGHT SIDE */}

          <div className="p-10 md:p-16 flex flex-col justify-center">

            <h2 className="text-pink-500 font-extrabold text-2xl mb-3">
              🚀 SkyRoute
            </h2>

            <h1 className="text-5xl font-extrabold text-[#2b2b35] mb-4 leading-tight">
              Log in to your account
            </h1>

            <p className="text-gray-500 text-lg mb-10 leading-8">
              Enter your email and password to access your dashboard.
            </p>

            <form className="space-y-6">

              <div>
                <label className="block text-sm font-bold mb-3 text-[#2b2b35]">
                  Email Address
                </label>

                <input
                  type="email"
                  placeholder="student@example.com"
                  className="w-full border border-pink-100 rounded-2xl px-5 py-4 outline-none focus:border-pink-400 transition"
                />
              </div>

              <div>
                <label className="block text-sm font-bold mb-3 text-[#2b2b35]">
                  Password
                </label>

                <input
                  type="password"
                  placeholder="••••••••"
                  className="w-full border border-pink-100 rounded-2xl px-5 py-4 outline-none focus:border-pink-400 transition"
                />
              </div>

              <div className="flex items-center justify-between text-sm">

                <label className="flex items-center gap-2 text-gray-500">
                  <input type="checkbox" />
                  Remember me
                </label>

                <button
                  type="button"
                  className="text-pink-500 font-semibold hover:underline"
                >
                  Forgot password?
                </button>

              </div>

              <button
                type="button"
                onClick={() => {
                  localStorage.setItem("isLoggedIn", "true")
                  window.location.href = "/student/dashboard"
                }}
                className="w-full bg-pink-500 text-white py-4 rounded-2xl font-extrabold text-lg shadow-lg hover:bg-pink-600 transition"
              >
                Log in
              </button>

            </form>

            <div className="flex items-center gap-4 my-8">
              <div className="flex-1 h-[1px] bg-gray-200"></div>

              <span className="text-gray-400 text-sm">
                or continue with
              </span>

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

            <p className="text-center text-gray-500 mt-10">
              Don’t have an account?{" "}

              <span className="text-pink-500 font-bold cursor-pointer hover:underline">
                Sign up
              </span>
            </p>

          </div>

        </div>

      </div>
    </>
  )
}