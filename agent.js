document.addEventListener("DOMContentLoaded", function () {

    // تبويبات All open / Unassigned / Breaching SLA / Assigned to me
    window.wireSimpleTabs("#viewTabs");

    // زرار Export
    const exportBtn = document.getElementById("exportBtn");
    if (exportBtn) {
        exportBtn.addEventListener("click", () => window.showToast("Exporting tickets..."));
    }

    // شريط الإجراءات الجماعية: يظهر حسب عدد التذاكر المحددة
    const checks = document.querySelectorAll(".row-check");
    const bulkBar = document.getElementById("bulkBar");
    const bulkCount = document.getElementById("bulkCount");

    function updateBulkBar() {
        const selected = document.querySelectorAll(".row-check:checked").length;
        if (selected > 0) {
            bulkBar.classList.add("show");
            bulkCount.textContent = selected + " selected";
        } else {
            bulkBar.classList.remove("show");
        }
        checks.forEach(c => {
            const row = c.closest("tr");
            row.classList.toggle("row-selected", c.checked);
        });
    }

    checks.forEach(c => c.addEventListener("change", updateBulkBar));
    updateBulkBar();

});
