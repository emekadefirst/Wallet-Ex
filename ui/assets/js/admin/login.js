document.getElementById("login-form").addEventListener("submit", async (e) => {
    e.preventDefault();
    
    const errorMessage = document.getElementById("error-message");
    const successMessage = document.getElementById("success-message");
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    // Hide any existing messages
    errorMessage.style.display = "none";
    successMessage.style.display = "none";

    try {
        const response = await fetch(
          "https://socialist-hannie-emekadefirst-e06c855d.koyeb.app/auth/admin-login",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ username, password }),
          }
        );

        if (response.ok) {
            const data = await response.json();

            // Store user data securely
            const userData = {
                id: data.data.id,
                username: data.data.username,
                email: data.data.email,
                is_verified: data.data.is_staff
            };

            Object.entries(userData).forEach(([key, value]) => {
                sessionStorage.setItem(key, value);
            });
            successMessage.style.display = "block";
            
            setTimeout(() => {
                window.location.href = "admin_dashboard.html";
            }, 1500);
        } else {
            const errorData = await response.json();
            errorMessage.textContent = errorData.detail || "Login failed. Please try again.";
            errorMessage.style.display = "block";
        }
    } catch (error) {
        console.error("Error:", error);
        errorMessage.textContent = "Connection error. Please try again later.";
        errorMessage.style.display = "block";
    }
});