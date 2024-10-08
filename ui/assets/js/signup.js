const liveUrl = "https://socialist-hannie-emekadefirst-e06c855d.koyeb.app";
const testUrl = "http://127.0.0.1:8000";

// Helper function to show error messages
const showError = (elementId, message) => {
  const errorElement = document.getElementById(elementId);
  if (errorElement) {
    errorElement.textContent = message;
    errorElement.style.display = message ? "block" : "none";
  }
};

// Helper function to clear all error messages
const clearErrors = () => {
  const errorIds = [
    "username-error",
    "email-error",
    "password-error",
    "confirm-password-error",
  ];
  errorIds.forEach((id) => showError(id, ""));
};

const signupForm = document.getElementById("signupForm");
if (signupForm) {
  signupForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    clearErrors();

    const username = document.getElementById("username")?.value?.trim();
    const email = document.getElementById("email")?.value?.trim();
    const password = document.getElementById("password")?.value;
    const confirmPassword = document.getElementById("confirmPassword")?.value;

    // Validation
    let hasError = false;
    if (!username) {
      showError("username-error", "Username is required");
      hasError = true;
    }

    if (!email) {
      showError("email-error", "Email is required");
      hasError = true;
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        showError("email-error", "Please enter a valid email address");
        hasError = true;
      }
    }

    if (!password) {
      showError("password-error", "Password is required");
      hasError = true;
    }

    if (password !== confirmPassword) {
      showError("confirm-password-error", "Passwords do not match");
      hasError = true;
    }

    if (hasError) return;

    try {
      const submitButton = signupForm.querySelector(".signup-button");
      submitButton.disabled = true;
      submitButton.textContent = "Creating Account...";

      const response = await fetch(`${testUrl}/auth/signup`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, email, password }),
      });

      const data = await response.json();

      if (response.ok && data.status === 201) {
        // Store user data according to the actual response format
        const sessionData = {
          access_token: data.access_token,
        };

        Object.entries(sessionData).forEach(([key, value]) => {
          if (value !== undefined) {
            sessionStorage.setItem(key, value);
          }
        });

        // Success - redirect to index
        window.location.href = "index.html";
      } else {
        // Handle different types of errors
        if (data.detail) {
          if (data.detail.includes("email")) {
            showError("email-error", data.detail);
          } else if (data.detail.includes("username")) {
            showError("username-error", data.detail);
          } else {
            showError("username-error", data.detail);
          }
        } else {
          showError("username-error", "An error occurred during signup");
        }
      }
    } catch (error) {
      console.error("Error during signup:", error);
      showError("username-error", "Network error. Please try again later.");
    } finally {
      const submitButton = signupForm.querySelector(".signup-button");
      submitButton.disabled = false;
      submitButton.textContent = "Create Account";
    }
  });
} else {
  console.warn("Signup form not found in the document");
}
