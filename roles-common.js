// أدوات مشتركة لكل صفحات الأدوار الجديدة (Agent / Technician / Manager / Auditor)

// رسالة تنبيه صغيرة أسفل الشاشة (نفس شكل التوست المستخدم في باقي البروجكت)
window.showToast = window.showToast || function (message) {
    let toast = document.querySelector(".app-toast");
    if (!toast) {
        toast = document.createElement("div");
        toast.className = "app-toast";
        document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add("show");
    clearTimeout(window.__toastTimer);
    window.__toastTimer = setTimeout(() => toast.classList.remove("show"), 2500);
};

// تفعيل مجموعة أزرار من نوع segmented-toggle أو text-tabs (بيحطلها active بس، من غير فلترة بيانات حقيقية)
window.wireSimpleTabs = function (selector) {
    document.querySelectorAll(selector).forEach(group => {
        group.querySelectorAll("button").forEach(btn => {
            btn.addEventListener("click", function () {
                group.querySelectorAll("button").forEach(b => b.classList.remove("active"));
                this.classList.add("active");
            });
        });
    });
};

// أزرار عامة لسه مش متوصلة ببيانات حقيقية: بتظهر رسالة توضيحية بس
window.wireDemoButtons = function (selector, message) {
    document.querySelectorAll(selector).forEach(btn => {
        btn.addEventListener("click", function (e) {
            e.stopPropagation();
            window.showToast(message || "This action isn't wired up in the demo yet.");
        });
    });
};

document.addEventListener("DOMContentLoaded", function () {
    // زرار تسجيل الخروج المشترك في كل الـ sidebars
    document.querySelectorAll(".logout-btn").forEach(btn => {
        btn.addEventListener("click", function () {
            window.location.href = "index.html";
        });
    });
});
