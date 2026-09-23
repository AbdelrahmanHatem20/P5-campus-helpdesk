// ===== Fixline – Create Ticket =====

document.addEventListener("DOMContentLoaded", function () {
    // أزرار درجة الاستعجال
    const urgencyButtons = document.querySelectorAll(".urgency-btn");
    let selectedUrgency = "Medium";

    urgencyButtons.forEach(button => {
        button.addEventListener("click", function () {
            urgencyButtons.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");
            selectedUrgency = this.getAttribute("data-value");
        });
    });

    // لو الرابط فيه ?edit=ID بنفتح الفورم في وضع التعديل ونعبي البيانات
    const params = new URLSearchParams(window.location.search);
    const editId = params.get("edit");
    const editingTicket = editId && window.getTicketById ? window.getTicketById(editId) : null;

    if (editingTicket) {
        const heading = document.getElementById("pageHeading");
        const subtitle = document.getElementById("pageSubtitle");
        const submitBtn = document.getElementById("submitBtn");

        if (heading) heading.textContent = "Edit ticket";
        if (subtitle) subtitle.textContent = "Update the details of your ticket.";
        if (submitBtn) submitBtn.textContent = "Save changes";

        document.getElementById("ticketTitle").value = editingTicket.title || "";
        document.getElementById("ticketLocation").value = editingTicket.location || "";
        document.getElementById("ticketCategory").value = editingTicket.category || "IT & Computers";
        document.getElementById("ticketDesc").value = editingTicket.description || "";

        selectedUrgency = editingTicket.urgency || "Medium";
        urgencyButtons.forEach(btn => {
            btn.classList.toggle("active", btn.getAttribute("data-value") === selectedUrgency);
        });
    }

    // زرار Cancel: يرجع لصفحة التذكرة لو بنعدل، أو للداشبورد لو تذكرة جديدة
    const cancelBtn = document.getElementById("cancelBtn");
    if (cancelBtn) {
        cancelBtn.addEventListener("click", function () {
            window.location.href = editingTicket
                ? "ticket-details.html?id=" + encodeURIComponent(editingTicket.id)
                : "dashboard.html";
        });
    }

    // إرسال النموذج
    const ticketForm = document.getElementById("ticketForm");
    if (!ticketForm) return;

    ticketForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const titleInput = document.getElementById("ticketTitle");
        const locationInput = document.getElementById("ticketLocation");
        const titleError = document.getElementById("titleError");
        const locationError = document.getElementById("locationError");

        const title = titleInput.value.trim();
        const location = locationInput.value.trim();
        const category = document.getElementById("ticketCategory").value;
        const description = document.getElementById("ticketDesc").value.trim();

        // التحقق من الحقول المطلوبة
        let isValid = true;

        if (title === "") {
            titleError.textContent = "Please fill out this field.";
            titleInput.classList.add("invalid");
            isValid = false;
        } else {
            titleError.textContent = "";
            titleInput.classList.remove("invalid");
        }

        if (location === "") {
            locationError.textContent = "Please fill out this field.";
            locationInput.classList.add("invalid");
            isValid = false;
        } else {
            locationError.textContent = "";
            locationInput.classList.remove("invalid");
        }

        if (!isValid) return;

        const now = new Date();
        const date = "Today, " + now.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

        if (editingTicket) {
            // تعديل تذكرة موجودة: نحافظ على الـ id والحالة والتاريخ الأصليين
            const updatedTicket = Object.assign({}, editingTicket, {
                title: title,
                category: category,
                location: location,
                urgency: selectedUrgency,
                description: description || "No description provided."
            });

            window.saveOrUpdateTicket(updatedTicket);
            window.location.href = "ticket-details.html?id=" + encodeURIComponent(updatedTicket.id);
            return;
        }

        const newTicket = {
            id: nextTicketId(),
            title: title,
            category: category,
            location: location,
            urgency: selectedUrgency,
            description: description || "No description provided.",
            status: "In progress",
            assignedTo: "Maintenance Team",
            date: date
        };

        const savedTickets = getUserTickets();
        savedTickets.unshift(newTicket);
        saveUserTickets(savedTickets);

        window.location.href = "dashboard.html";
    });
});
