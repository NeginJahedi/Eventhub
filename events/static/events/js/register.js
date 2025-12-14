const form = document.querySelector(".auth-form");

form.addEventListener("submit", (e) => {
  let valid = true;

  document.querySelectorAll(".field").forEach(field => {
    const input = field.querySelector("input");
    const error = field.querySelector(".error");
    error.style.display = "none";

    if (!input.value.trim()) {
      error.textContent = "This field is required";
      error.style.display = "block";
      valid = false;
    }
  });

  if (!valid) e.preventDefault();
});
