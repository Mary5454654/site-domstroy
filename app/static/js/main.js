const accessButton = document.querySelector("[data-access-toggle]");
const savedMode = localStorage.getItem("accessMode");

if (savedMode === "enabled") {
    document.body.classList.add("access-mode");
}

if (accessButton) {
    accessButton.addEventListener("click", () => {
        document.body.classList.toggle("access-mode");
        const enabled = document.body.classList.contains("access-mode");
        localStorage.setItem("accessMode", enabled ? "enabled" : "disabled");
    });
}

