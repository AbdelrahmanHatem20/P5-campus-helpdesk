// ===== Fixline – بيانات التذاكر المشتركة بين الصفحات =====

// تذاكر تجريبية عشان الصفحة تبان مليانة حتى قبل ما المستخدم يعمل تذكرة جديدة
window.SEED_TICKETS = [
    {
        id: "TCK-2041",
        title: "AC not cooling in Meeting Room 3",
        category: "Maintenance & Facilities",
        location: "Building B · 3.12",
        urgency: "High",
        description: "The AC in Meeting Room 3 is running but the room stays warm. Please check the unit and the thermostat.",
        status: "In progress",
        date: "Today, 09:15",
        assignedTo: "Karim Adel",
        note: "Karim Adel is working on it."
    },
    {
        id: "TCK-2031",
        title: "Replace broken office chair",
        category: "Maintenance & Facilities",
        location: "Building A · Room 210",
        urgency: "Low",
        description: "The chair in office A-210 has a broken hydraulic cylinder and keeps sinking while sitting.",
        status: "Resolved",
        date: "Yesterday, 16:20",
        assignedTo: "Maintenance Team",
        note: "Chair replaced. Please confirm the fix so we can close the ticket."
    },
    {
        id: "TCK-2035",
        title: "Projector in Hall 101 won't turn on",
        category: "IT & Computers",
        location: "Building C · Hall 101",
        urgency: "Medium",
        description: "The projector shows a red light and does not respond to the remote or the power button.",
        status: "New",
        date: "Yesterday, 11:05",
        assignedTo: "Unassigned",
        note: "Your ticket is logged and queued for a technician."
    }
];

// تذاكر المستخدم المحفوظة في المتصفح
window.getUserTickets = function () {
    try {
        return JSON.parse(localStorage.getItem("userTickets")) || [];
    } catch (e) {
        return [];
    }
};

window.saveUserTickets = function (list) {
    localStorage.setItem("userTickets", JSON.stringify(list));
};

// التذاكر التجريبية (Seed) اللي المستخدم مسحها، عشان متطلعش تاني
window.getDeletedSeedIds = function () {
    try {
        return JSON.parse(localStorage.getItem("deletedSeedTickets")) || [];
    } catch (e) {
        return [];
    }
};

// كل التذاكر (تذاكر المستخدم أولاً ثم التجريبية) – نفس المصدر لكل الصفحات
window.getAllTickets = function () {
    const users = window.getUserTickets();
    const seedIds = window.SEED_TICKETS.map(t => t.id);
    const deletedSeeds = window.getDeletedSeedIds();

    const userList = users.map(t =>
        Object.assign({}, t, { userMade: seedIds.indexOf(t.id) === -1 })
    );

    const seedList = window.SEED_TICKETS
        .filter(seed => !users.some(u => u.id === seed.id) && deletedSeeds.indexOf(seed.id) === -1)
        .map(t => Object.assign({}, t, { userMade: false }));

    return userList.concat(seedList);
};

window.getTicketById = function (id) {
    return window.getAllTickets().find(t => t.id === id) || null;
};

// يحفظ تذكرة جديدة أو يحدّث تذكرة موجودة بنفس الـ id (يستخدمها فورم التعديل)
window.saveOrUpdateTicket = function (ticket) {
    const list = window.getUserTickets();
    const idx = list.findIndex(t => t.id === ticket.id);
    if (idx !== -1) {
        list[idx] = ticket;
    } else {
        list.unshift(ticket);
    }
    window.saveUserTickets(list);
};

// يمسح تذكرة نهائيًا (سواء كانت اتعملت من المستخدم أو من التذاكر التجريبية)
window.deleteTicket = function (id) {
    const remaining = window.getUserTickets().filter(t => t.id !== id);
    window.saveUserTickets(remaining);

    const seedIds = window.SEED_TICKETS.map(t => t.id);
    if (seedIds.indexOf(id) !== -1) {
        const deleted = window.getDeletedSeedIds();
        if (deleted.indexOf(id) === -1) {
            deleted.push(id);
            localStorage.setItem("deletedSeedTickets", JSON.stringify(deleted));
        }
    }
};

// توليد ID جديد من غير تكرار
window.nextTicketId = function () {
    const existing = window.getAllTickets().map(t => t.id);
    let id;
    do {
        id = "TCK-" + (3000 + Math.floor(Math.random() * 900));
    } while (existing.indexOf(id) !== -1);
    return id;
};

// التذاكر اللي صاحبها أكد إنها اتحلت (Review Fix)
window.getConfirmedFixes = function () {
    try {
        return JSON.parse(localStorage.getItem("confirmedFixes")) || [];
    } catch (e) {
        return [];
    }
};

window.confirmFix = function (id) {
    const list = window.getConfirmedFixes();
    if (list.indexOf(id) === -1) list.push(id);
    localStorage.setItem("confirmedFixes", JSON.stringify(list));
};

// حماية من كسر الـ HTML بأي نص يكتبه المستخدم
window.escapeHtml = function (value) {
    return String(value == null ? "" : value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
};

// رسالة تنبيه صغيرة سفلية الشاشة
window.showToast = function (message) {
    document.querySelectorAll(".app-toast").forEach(t => t.remove());
    const toast = document.createElement("div");
    toast.className = "app-toast";
    toast.textContent = message;
    document.body.appendChild(toast);
    requestAnimationFrame(() => toast.classList.add("show"));
    setTimeout(() => {
        toast.classList.remove("show");
        setTimeout(() => toast.remove(), 300);
    }, 2600);
};
