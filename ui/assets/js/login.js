const liveUrl = "https://socialist-hannie-emekadefirst-e06c855d.koyeb.app";
const testUrl = "http://127.0.0.1:8000";

document.querySelector(".login-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch(
      "https://socialist-hannie-emekadefirst-e06c855d.koyeb.app/auth/login",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      }
    );

    if (response.ok) {
      const data = await response.json();

      // Store relevant data in sessionStorage
      sessionStorage.setItem("access_token", data.access_token);
      sessionStorage.setItem("user_id", data.user_id.id);
      sessionStorage.setItem("username", data.user_id.username);
      sessionStorage.setItem("email", data.user_id.email);
      sessionStorage.setItem("is_verified", data.user_id.is_verified);
      sessionStorage.setItem("token_type", data.token_type);

      alert("Login successful");
      window.location.href = "dashboard.html";
    } else {
      const errorData = await response.json();
      alert("Login failed: " + (errorData.detail || "Unknown error"));
    }
  } catch (error) {
    console.error("Error:", error);
    alert("User not found");
  }
});
