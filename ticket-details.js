// ===== Fixline – My Tickets (قائمة + تفاصيل) =====

document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const id = params.get("id");
    const ticket = id ? getTicketById(id) : null;

    const detailView = document.getElementById("detailView");
    const listView = document.getElementById("listView");

    if (ticket) {
        // فتح تفاصيل تذكرة محددة عبر ?id=
        if (listView) listView.style.display = "none";
        if (detailView) detailView.style.display = "";
        fillDetail(ticket);
    } else {
        // بدون ID (أو ID غير موجود): عرض كل التذاكر
        if (detailView) detailView.style.display = "none";
        if (listView) listView.style.display = "";
        renderList();
        if (id) showToast("Ticket not found. Showing all your tickets.");
    }
});

// رسم قائمة كل التذاكر
function renderList() {
    const wrap = document.getElementById("ticketsList");
    if (!wrap) return;

    const tickets = getAllTickets();

    if (tickets.length === 0) {
        wrap.innerHTML = `
            <div class="empty-state">
                <p>No tickets yet.</p>
                <a href="create-ticket.html">Create your first ticket</a>
            </div>`;
        return;
    }

    wrap.innerHTML = tickets.map(t => `
        <div class="ticket-list-card" onclick="window.location.href='ticket-details.html?id=${encodeURIComponent(t.id)}'">
            <div class="ticket-list-top">
                <span class="ticket-code">${window.escapeHtml(t.id)}</span>
                <span class="status-pill ${pillClass(t.status)}">${window.escapeHtml(t.status)}</span>
            </div>
            <h3 class="ticket-list-title">${window.escapeHtml(t.title)}</h3>
            <p class="ticket-list-desc">${window.escapeHtml(t.description || "")}</p>
            <div class="ticket-list-meta">
                <span>📍 ${window.escapeHtml(t.location || "—")}</span>
                <span>📅 ${window.escapeHtml(t.date || "—")}</span>
                <span>${window.escapeHtml(t.category || "")}</span>
            </div>
            <div class="ticket-list-actions">
                <button type="button" class="btn-edit-ticket" onclick="event.stopPropagation(); window.location.href='create-ticket.html?edit=${encodeURIComponent(t.id)}'">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4Z"></path></svg>
                    Edit
                </button>
                <button type="button" class="btn-delete-ticket" onclick="event.stopPropagation(); handleDeleteTicket('${t.id}')">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                    Delete
                </button>
            </div>
        </div>
    `).join("");
}

// مسح تذكرة بعد تأكيد المستخدم، وتحديث القائمة على طول
function handleDeleteTicket(id) {
    const confirmed = window.confirm("Delete this ticket? This can't be undone.");
    if (!confirmed) return;

    window.deleteTicket(id);
    renderList();
    if (window.showToast) window.showToast("Ticket deleted.");
}

function pillClass(status) {
    if (status === "New") return "st-new";
    if (status === "Resolved") return "st-resolved";
    if (status === "Closed") return "st-closed";
    return "";
}

// ملء صفحة التفاصيل ببيانات التذكرة المختارة
function fillDetail(ticket) {
    setText("detailTitle", ticket.title);
    setText("detailId", ticket.id);
    setText("detailStatus", ticket.status);
    setText("detailDescription", ticket.description || "No description provided.");
    setText("detailCategory", ticket.category || "—");
    setText("detailLocation", ticket.location || "—");
    setText("detailSubmitted", ticket.date || "—");

    // شارة الحالة
    const pill = document.getElementById("detailStatus");
    if (pill) pill.className = "status-pill " + pillClass(ticket.status);

    // درجة الاستعجال ولون النقطة
    const urgencyEl = document.getElementById("detailUrgency");
    const urgencyColors = { Low: "#16a34a", Medium: "#d97706", High: "#dc2626", Critical: "#7f1d1d" };
    if (urgencyEl) {
        const urgency = ticket.urgency || "Medium";
        urgencyEl.innerHTML =
            `<span class="urgency-dot" style="background-color: ${urgencyColors[urgency] || "#d97706"};"></span> ${window.escapeHtml(urgency)}`;
    }

    // خطوات التقدم
    renderSteps(ticket.status);

    // ملاحظة الفني
    const defaultNote =
        ticket.status === "New" ? "Your ticket is logged and queued for a technician."
        : ticket.status === "Resolved" ? "The issue has been fixed. Please confirm."
        : "The maintenance team is working on it.";
    setText("detailTechnicianNote", ticket.note || defaultNote);

    // عداد الـ SLA
    const targets = { Low: 48, Medium: 24, High: 8, Critical: 2 };
    const hours = targets[ticket.urgency] || 24;

    let pct, leftText, fillColor = "#f59e0b";
    if (ticket.status === "Resolved" || ticket.status === "Closed") {
        pct = 100;
        leftText = "Resolved in time";
        fillColor = "#16a34a";
    } else if (ticket.status === "New") {
        pct = 15;
        leftText = hours + " h left";
    } else {
        pct = 70;
        leftText = Math.max(1, Math.round(hours * 0.3)) + " h left";
    }

    setText("slaTimeVal", leftText);
    setText("slaTargetText", "Target: " + hours + " h from submission");

    const fill = document.getElementById("slaProgressFill");
    if (fill) {
        fill.style.width = pct + "%";
        fill.style.backgroundColor = fillColor;
    }

    // سجل النشاط
    renderActivity(ticket);
}

function setText(id, value) {
    const el = document.getElementById(id);
    if (el) el.textContent = value;
}

// رسم خطوات New → In Progress → Resolved حسب حالة التذكرة
function renderSteps(status) {
    const container = document.getElementById("stepsContainer");
    if (!container) return;

    const labels = ["New", "In Progress", "Resolved"];
    const currentIndex =
        status === "New" ? 0 :
        status === "In progress" ? 1 : 2;
    const isDone = status === "Resolved" || status === "Closed";

    const checkSvg = `<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
    const spinnerSvg = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M21 12a9 9 0 1 1-6.219-8.56"></path></svg>`;

    container.innerHTML = labels.map((label, i) => {
        let cls = "step-node";
        let inner = "";

        if (isDone || i < currentIndex) {
            cls += " completed";
            inner = checkSvg;
        } else if (i === currentIndex) {
            cls += " active";
            inner = spinnerSvg;
        }

        return `
            <div class="${cls}">
                <div class="node-circle">${inner}</div>
                <span class="node-text">${label}</span>
            </div>`;
    }).join("");
}

// رسم سجل النشاط
function renderActivity(ticket) {
    const list = document.getElementById("activityList");
    if (!list) return;

    const assigned = ticket.assignedTo || "Maintenance Team";

    const firstDesc =
        ticket.status === "New" ? "Ticket received and is waiting to be picked up."
        : ticket.status === "Resolved" || ticket.status === "Closed"
            ? "Completed the fix and marked the ticket as resolved."
            : "Picked up the ticket and checking the reported issue.";

    list.innerHTML = `
        <div class="activity-row">
            <div class="activity-bullet blue-dot"></div>
            <div class="activity-info">
                <p class="activity-head">${window.escapeHtml(assigned)} <span class="activity-time">· ${window.escapeHtml(ticket.date || "Just now")}</span></p>
                <p class="activity-desc">${firstDesc}</p>
            </div>
        </div>
        <div class="activity-row" style="margin-bottom: 0;">
            <div class="activity-bullet gray-dot"></div>
            <div class="activity-info">
                <p class="activity-head">You <span class="activity-time">· Submitted</span></p>
                <p class="activity-desc">Ticket ${window.escapeHtml(ticket.id)} successfully created and logged.</p>
            </div>
        </div>
    `;
}
