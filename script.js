// خريطة الإيميلات على أدوار المستخدمين المختلفة
const ROLE_ROUTES = {
    "nour.202354848@bua.edu.eg": "dashboard.html",        // Reporter
    "omar.farouk@bua.edu.eg": "agent-dashboard.html",      // Helpdesk Agent
    "karim.adel@bua.edu.eg": "tech-dashboard.html",        // Technician
    "mona.saleh@bua.edu.eg": "manager-dashboard.html",     // Service Manager
    "youssef.nabil@bua.edu.eg": "audit-log.html"           // Auditor
};

// دالة معالجة نموذج تسجيل الدخول والانتقال للداش بورد المناسب حسب الإيميل
function handleLogin(event) {
    event.preventDefault();
    
    const emailInput = document.getElementById('email');
    const emailError = document.getElementById('emailError');
    
    const passwordInput = document.getElementById('password');
    const passwordError = document.getElementById('passwordError');
    
    let isValid = true;
    
    // التحقق من حقل الإيميل
    if (emailInput.value.trim() === "") {
        emailError.textContent = "Please fill out this field.";
        emailInput.style.borderColor = "#d9534f";
        isValid = false;
    } else {
        emailError.textContent = "";
        emailInput.style.borderColor = "#11223b";
    }
    
    // التحقق من حقل الباسورد
    if (passwordInput.value.trim() === "") {
        passwordError.textContent = "Please fill out this field.";
        passwordInput.style.borderColor = "#d9534f";
        isValid = false;
    } else {
        passwordError.textContent = "";
        passwordInput.style.borderColor = "#11223b";
    }
    
    // لو كل الحقول مليانة، نوديه على الصفحة المناسبة لدوره حسب الإيميل
    if (isValid) {
        const email = emailInput.value.trim().toLowerCase();
        const destination = ROLE_ROUTES[email] || "dashboard.html"; // أي إيميل مش معروف بيدخل كـ Reporter افتراضيًا
        window.location.href = destination;
    }
}

// أزرار صفحة تسجيل الدخول
document.addEventListener("DOMContentLoaded", function () {
    // زرار Let's Start ينقلك لمربع الإيميل
    const startBtn = document.getElementById("letsStartBtn");
    if (startBtn) {
        startBtn.addEventListener("click", function () {
            const emailInput = document.getElementById("email");
            if (emailInput) emailInput.focus();
        });
    }

    // زرار Continue with University (دخول تجريبي)
    const ssoBtn = document.getElementById("ssoBtn");
    if (ssoBtn) {
        ssoBtn.addEventListener("click", function () {
            window.location.href = "dashboard.html";
        });
    }
});