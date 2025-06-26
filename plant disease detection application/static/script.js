document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const spinner = document.getElementById("spinner");

    form.addEventListener("submit", function () {
        spinner.style.display = "block";  // Show spinner on submit
    });
});