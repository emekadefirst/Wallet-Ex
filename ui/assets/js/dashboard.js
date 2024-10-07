// Mobile menu toggle
document.addEventListener("DOMContentLoaded", () => {
  const menuToggle = document.createElement("button");
  menuToggle.classList.add("menu-toggle");
  menuToggle.innerHTML = '<i class="fas fa-bars"></i>';
  menuToggle.style.position = "fixed";
  menuToggle.style.top = "1rem";
  menuToggle.style.left = "1rem";
  menuToggle.style.zIndex = "2000";
  menuToggle.style.padding = "0.5rem";
  menuToggle.style.background = "var(--primary-color)";
  menuToggle.style.border = "none";
  menuToggle.style.borderRadius = "8px";
  menuToggle.style.color = "white";
  menuToggle.style.display = "none";

  document.body.appendChild(menuToggle);

  const sidebar = document.querySelector(".sidebar");

  menuToggle.addEventListener("click", () => {
    sidebar.classList.toggle("active");
  });

  const checkWidth = () => {
    if (window.innerWidth <= 768) {
      menuToggle.style.display = "block";
    } else {
      menuToggle.style.display = "none";
      sidebar.classList.remove("active");
    }
  };

  window.addEventListener("resize", checkWidth);
  checkWidth();
});

document.addEventListener("DOMContentLoaded", () => {
    const username = sessionStorage.getItem("username");
    const status = sessionStorage.getItem("is_verified");
    const mainContent = document.querySelector(".main-content");
    const transactionsSection = document.querySelector(".transactions");
    document.querySelector(".header h1").textContent = `Hi, ${
    username || "Guest"
    }`;

    if (status !== "true") {
    document.querySelector(".header span").textContent =
        "verify your account";
    document.querySelector(".card-number").textContent =
        "verify your account";
    document.querySelector(".balance-amount").textContent = "****";
    if (transactionsSection) {
        transactionsSection.remove();
    }
    const verificationSection = document.createElement("div");
    verificationSection.className = "transactions";
    verificationSection.style.textAlign = "center";
    verificationSection.style.padding = "2rem";

    verificationSection.innerHTML = `
        <h2>Account Verification Required</h2>
        <p style="margin: 1rem 0; color: var(--text-secondary)">
            Please verify your account to view your transaction history and unlock all features.
        </p>
        <button id="verifyButton" style="
            background: var(--primary-color);
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 500;
            margin-top: 1rem;
            transition: background 0.3s ease;
        ">
            Verify Account
        </button>
    `;

    mainContent.appendChild(verificationSection);

    // Add click event for verify button
    document.getElementById("verifyButton").addEventListener("click", () => {
        window.location.href = "verify.html";
    });
    }
});