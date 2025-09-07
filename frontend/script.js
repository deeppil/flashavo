// Simple login/register (localStorage mock)
function login() {
  const user = document.getElementById("login-username").value;
  const pass = document.getElementById("login-password").value;
  if (localStorage.getItem(user) === pass) {
    localStorage.setItem("loggedInUser", user);
    window.location.href = "index.html";
  } else {
    alert("Invalid credentials!");
  }
}

function registerUser() {
  const user = document.getElementById("register-username").value;
  const pass = document.getElementById("register-password").value;
  if (user == "" && pass == "") {
    alert("Please enter a username and password!");
  } else {
    localStorage.setItem(user, pass); 
    alert("Registration successful! Please login.");
    window.location.href = "login.html";
  }
}

