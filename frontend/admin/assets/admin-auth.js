/* Shared admin auth helpers */

function getAdminToken() {
  return localStorage.getItem("kanya_admin_token");
}

function requireAdminAuth() {
  const token = getAdminToken();
  if (!token) {
    window.location.href = "login.html";
    return null;
  }
  return token;
}

function adminLogout() {
  localStorage.removeItem("kanya_admin_token");
  window.location.href = "login.html";
}

/** Authenticated API request. Redirects to login on 401. */
async function adminApiRequest(path, options = {}) {
  const token = getAdminToken();
  const headers = { ...(options.headers || {}) };
  if (!(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const res = await fetch(`${CONFIG.API_BASE_URL}${path}`, { ...options, headers });

  if (res.status === 401) {
    localStorage.removeItem("kanya_admin_token");
    window.location.href = "login.html";
    throw new Error("Session expired. Please log in again.");
  }

  let data = null;
  try { data = await res.json(); } catch (e) { /* no body */ }

  if (!res.ok) {
    const message = (data && (data.detail || data.message)) || "Something went wrong.";
    throw new Error(typeof message === "string" ? message : "Something went wrong.");
  }
  return data;
}
