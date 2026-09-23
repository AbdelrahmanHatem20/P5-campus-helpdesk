// بيانات ثابتة تمثل تفاصيل كل حدث في الـ Audit log (متطابقة مع صفوف الجدول بالترتيب)
const AUDIT_EVENTS = [
    {
        action: "Status changed",
        ticket: "TCK-2041",
        by: "Karim Adel · Technician",
        time: "Sep 3, 10:42:05",
        ip: "10.24.8.19",
        change: "Status: In progress → Resolved"
    },
    {
        action: "Assigned technician",
        ticket: "TCK-2041",
        by: "Omar Farouk · Helpdesk Agent",
        time: "Sep 3, 09:15:22",
        ip: "10.24.8.17",
        change: "Assigned to: — → Karim Adel"
    },
    {
        action: "Priority changed",
        ticket: "TCK-2041",
        by: "Omar Farouk · Helpdesk Agent",
        time: "Sep 3, 09:12:40",
        ip: "10.24.8.17",
        change: "Priority: Medium → High"
    },
    {
        action: "Ticket created",
        ticket: "TCK-2041",
        by: "Nour Hassan · Reporter",
        time: "Sep 3, 08:58:03",
        ip: "10.24.9.02",
        change: "New ticket submitted"
    },
    {
        action: "SLA policy edited",
        ticket: "High priority",
        by: "Hana Mostafa · Service Manager",
        time: "Sep 2, 16:20:11",
        ip: "10.24.6.44",
        change: "Resolution target: 12 hours → 8 hours"
    }
];

function renderEventDetails(eventData) {
    const wrap = document.getElementById("eventDetails");
    if (!wrap) return;

    wrap.innerHTML = `
        <div>
            <div class="ed-label">Action</div>
            <div class="ed-value">${eventData.action}</div>
        </div>
        <div>
            <div class="ed-label">Ticket</div>
            <div class="ed-value">${eventData.ticket}</div>
        </div>
        <div>
            <div class="ed-label">By</div>
            <div class="ed-value">${eventData.by}</div>
        </div>
        <div>
            <div class="ed-label">Time</div>
            <div class="ed-value">${eventData.time}</div>
        </div>
        <div>
            <div class="ed-label">IP address</div>
            <div class="ed-value">${eventData.ip}</div>
        </div>
        <div class="change-box">
            <div class="ed-label">Change</div>
            <div class="ed-value" style="font-weight:500;">${eventData.change}</div>
        </div>
    `;
}

document.addEventListener("DOMContentLoaded", function () {
    const rows = document.querySelectorAll(".audit-table-row");

    rows.forEach(row => {
        row.addEventListener("click", function () {
            rows.forEach(r => r.classList.remove("row-selected"));
            this.classList.add("row-selected");
            const idx = parseInt(this.dataset.index, 10);
            renderEventDetails(AUDIT_EVENTS[idx]);
        });
    });

    // نعرض تفاصيل الصف اللي متحدد بالفعل (index 1) أول ما الصفحة تفتح
    if (rows.length) {
        renderEventDetails(AUDIT_EVENTS[1]);
    }
});
