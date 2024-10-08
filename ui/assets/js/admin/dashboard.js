// Add hover effect to menu items
document.querySelectorAll(".menu-item").forEach((item) => {
  item.addEventListener("click", function () {
    document
      .querySelectorAll(".menu-item")
      .forEach((i) => i.classList.remove("active"));
    this.classList.add("active");
  });
});

// Simulate loading data
setInterval(() => {
  const values = document.querySelectorAll(".value");
  values.forEach((value) => {
    if (value.innerText.includes("$")) {
      const newValue = "$" + (Math.random() * 100000).toFixed(0);
      value.innerText = newValue;
    } else if (!isNaN(value.innerText)) {
      const newValue = (Math.random() * 2000).toFixed(0);
      value.innerText = newValue;
    }
  });
}, 5000);
