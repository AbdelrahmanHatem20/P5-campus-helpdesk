document.addEventListener("DOMContentLoaded", function () {
    const activeTicketsCard = document.querySelector(".active-tickets-card");
    let savedTickets = JSON.parse(localStorage.getItem("userTickets")) || [];

    if (savedTickets.length > 0 && activeTicketsCard) {
        const cardHeader = activeTicketsCard.querySelector(".card-header");

        savedTickets.forEach(ticket => {
            const ticketHTML = `
                <div class="ticket-item">
                    <div class="ticket-info">
                        <span class="ticket-id">${ticket.id}</span>
                        <h4 class="ticket-title">${ticket.title}</h4>
                        <p class="ticket-desc" style="font-size: 13px; color: #475569; margin: 4px 0;">${ticket.description || ''}</p>
                        <span class="ticket-loc">${ticket.location} · Assigned to Maintenance Team</span>
                        <span class="ticket-date" style="font-size: 12px; color: #64748b; display: block; margin-top: 2px;">📅 Date: ${ticket.date || 'Today'}</span>
                        
                        <div class="ticket-progress-bars">
                            <span class="active"></span>
                            <span class="active"></span>
                            <span class="active"></span>
                            <span></span>
                            <span></span>
                        </div>
                    </div>
                    <span class="badge-status in-progress">In progress</span>
                </div>
            `;
            if (cardHeader) {
                cardHeader.insertAdjacentHTML("afterend", ticketHTML);
            }
        });
    }
});