const liveUrl = "https://socialist-hannie-emekadefirst-e06c855d.koyeb.app";
const testUrl = "http://127.0.0.1:8000";

document.querySelector(".login-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;
  const token = sessionStorage.getItem("access_token");

  try {
    const baseUrl =
      window.location.hostname === "127.0.0.1" ? testUrl : liveUrl;

    const response = await fetch(`${testUrl}/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        access_token: token,
      },
      body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
      const data = await response.json();

      // Store relevant data in sessionStorage
      sessionStorage.setItem("access_token", data.access_token);
      sessionStorage.setItem("user_id", data.data.id);
      sessionStorage.setItem("username", data.data.username);
      sessionStorage.setItem("email", data.data.email);
      sessionStorage.setItem("is_verified", data.data.is_verified);
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
