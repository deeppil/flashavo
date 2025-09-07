function login() {
  const user = document.getElementById("login-username").value.trim();
  const pass = document.getElementById("login-password").value.trim();

  if (!user || !pass) {
    alert("Enter both username and password!");
    return;
  }

  const storedPass = localStorage.getItem("user:" + user);
  if (storedPass && storedPass === pass) {
    localStorage.setItem("loggedInUser", user);
    window.location.href = "index.html";  // go to home
  } else {
    alert("Invalid username or password!");
  }
}

// --- REGISTER ---
function registerUser() {
  const user = document.getElementById("register-username").value.trim();
  const pass = document.getElementById("register-password").value.trim();

  if (!user || !pass) {
    alert("Please enter a username and password!");
    return;
  }

  if (localStorage.getItem("user:" + user)) {
    alert("User already exists! Try another username.");
    return;
  }

  localStorage.setItem("user:" + user, pass);
  alert("Registration successful! Please login.");
  window.location.href = "login.html";
}

// --- LOGOUT ---
function logout() {
  localStorage.removeItem("loggedInUser");
  window.location.href = "login.html";
}

// --- GUARD (put in protected pages) ---
function requireLogin() {
  const u = localStorage.getItem("loggedInUser");
  if (!u) {
    const next = encodeURIComponent(location.pathname);
    window.location.href = "login.html?next=" + next;
  }
}