// ==========================================
// (1) API Service Layer
// كل طلبات الـAPI بتتعمل من هنا
// ==========================================

const API_URL = "http://localhost:5001/api";

// ------------------------------------------
// (2) تخزين الـ Token بعد Login
// ------------------------------------------
function setToken(token) {
    localStorage.setItem("token", token);
}

function getToken() {
    return localStorage.getItem("token");
}

function clearToken() {
    localStorage.removeItem("token");
}

// ------------------------------------------
// Login — بيبعت الإيميل والباسورد للسيرفر
// ولو التوكن رجع نخزّنه في localStorage
// ------------------------------------------
async function login(email, password) {
    const res = await fetch(`${API_URL}/users/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });

    const data = await res.json();

    if (data && data.token) {
        setToken(data.token);
    }

    return data;
}

// ------------------------------------------
// (3) أي Request بعد كده لازم يبعت الـ Token
// في هيدر Authorization بالشكل: Bearer <token>
// ------------------------------------------
async function apiFetch(path, options = {}) {
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    const token = getToken();
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const res = await fetch(`${API_URL}${path}`, {
        ...options,
        headers: headers
    });

    return res.json();
}

// طلبات جاهزة يستخدمها باقي الصفحات
const getTickets = () => apiFetch("/tickets?limit=100");
const getCategories = () => apiFetch("/categories");

// نسجّلهم على window عشان باقي الملفات (script.js ... إلخ) تستخدمهم
window.ApiService = {
    API_URL: API_URL,
    login: login,
    apiFetch: apiFetch,
    getTickets: getTickets,
    getCategories: getCategories,
    getToken: getToken,
    setToken: setToken,
    clearToken: clearToken
};
