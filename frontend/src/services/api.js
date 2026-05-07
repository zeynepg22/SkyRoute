const API_BASE_URL = "http://localhost:8000";

export async function apiRequest(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
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