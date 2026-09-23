document.addEventListener("DOMContentLoaded", function () {

    // كل مجموعات التابز (7/14/30 يوم، Week/Month/Quarter...)
    window.wireSimpleTabs(".segmented-toggle");

    // صفوف التقارير المحفوظة
    document.querySelectorAll(".saved-report-row").forEach(row => {
        row.addEventListener("click", function () {
            window.showToast("Loading \"" + this.dataset.name + "\"...");
        });
    });

    // مفتاح التبديل (Automation toggle) - يشتغل بصريًا فقط
    document.querySelectorAll(".switch input").forEach(input => {
        input.addEventListener("change", function () {
            window.showToast(this.checked ? "Automation enabled." : "Automation disabled.");
        });
    });

});
