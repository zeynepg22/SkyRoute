const API_BASE_URL = "http://localhost:8000";

export async function apiRequest(endpoint, options = {}) {
  const token = localStorage.getItem("access_token");

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });

  if (!response.ok) {
    throw new Error("API request failed");
  }

  return response.json();
}

export const courseApi = {
  getCourses: () => apiRequest("/courses/"),
  getCourseById: (courseId) => apiRequest(`/courses/${courseId}`),
};

export const lessonApi = {
  getLesson: (lessonId) => apiRequest(`/lessons/${lessonId}`),

  getLessonsByCourse: (courseId) =>
    apiRequest(`/lessons/course/${courseId}`),
};

export const enrollmentApi = {
  enrollCourse: (courseId) =>
    apiRequest(`/enrollments/${courseId}`, {
      method: "POST",
    }),
};

export const progressApi = {
  completeLesson: (lessonId) =>
    apiRequest(`/progress/complete/${lessonId}`, {
      method: "POST",
    }),

  getProgress: (courseId) =>
    apiRequest(`/progress/${courseId}`),
};