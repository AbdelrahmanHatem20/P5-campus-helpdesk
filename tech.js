document.addEventListener("DOMContentLoaded", function () {

    const toggle = document.getElementById("viewToggle");
    const boardView = document.getElementById("boardView");
    const listView = document.getElementById("listView");

    if (toggle) {
        toggle.querySelectorAll("button").forEach(btn => {
            btn.addEventListener("click", function () {
                toggle.querySelectorAll("button").forEach(b => b.classList.remove("active"));
                this.classList.add("active");

                if (this.dataset.view === "board") {
                    boardView.style.display = "grid";
                    listView.style.display = "none";
                } else {
                    boardView.style.display = "none";
                    listView.style.display = "block";
                }
            });
        });
    }

});
