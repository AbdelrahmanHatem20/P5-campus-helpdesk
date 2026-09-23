document.addEventListener("DOMContentLoaded", function () {
    const notifCardBox = document.querySelector(".notif-card-box");
    if (!notifCardBox) return;

    let savedTickets = JSON.parse(localStorage.getItem("userTickets")) || [];
    let customNotifs = JSON.parse(localStorage.getItem("fixline_notifications")) || [];

    let htmlContent = `<div class="section-title">Today</div>`;

    // جلب التذاكر المسجلة وعرضها كإشعارات جديدة متزامنة
    if (savedTickets.length > 0) {
        savedTickets.forEach(ticket => {
            htmlContent += `
                <div class="notif-item">
                    <div class="notif-icon-wrap">🔔</div>
                    <div class="notif-text">
                        <p>تم تسجيل التذكرة ${ticket.id} (${ticket.title}) بنجاح</p>
                        <span class="notif-time">${ticket.date || 'الآن'}</span>
                    </div>
                    <span class="blue-dot"></span>
                </div>
            `;
        });
    }

    // جلب أي إشعارات إضافية مخزنة
    if (customNotifs.length > 0) {
        customNotifs.forEach(notif => {
            htmlContent += `
                <div class="notif-item">
                    <div class="notif-icon-wrap">🔔</div>
                    <div class="notif-text">
                        <p>${notif.text}</p>
                        <span class="notif-time">${notif.time}</span>
                    </div>
                    <span class="blue-dot"></span>
                </div>
            `;
        });
    }

    // العناصر الثابتة الأصلية للمحافظة على شكل التصميم تماماً دون أي نقصان
    htmlContent += `
        <div class="notif-item">
            <div class="notif-icon-wrap">🔔</div>
            <div class="notif-text">
                <p>Karim Adel started work on TCK-2041</p>
                <span class="notif-time">10:42</span>
            </div>
            <span class="blue-dot"></span>
        </div>
        <div class="notif-item">
            <div class="notif-icon-wrap">🔔</div>
            <div class="notif-text">
                <p>TCK-2031 was marked resolved. Please confirm the fix.</p>
                <span class="notif-time">10:42</span>
            </div>
            <span class="blue-dot"></span>
        </div>
        <div class="notif-item">
            <div class="notif-icon-wrap">🔔</div>
            <div class="notif-text">
                <p>Omar Farouk assigned TCK-2041 to Karim Adel</p>
                <span class="notif-time">09:15</span>
            </div>
        </div>
        <div class="section-title earlier-title">Earlier</div>
        <div class="notif-item">
            <div class="notif-icon-wrap">🔔</div>
            <div class="notif-text">
                <p>TCK-2029 was closed</p>
                <span class="notif-time">Yesterday</span>
            </div>
        </div>
        <div class="notif-item">
            <div class="notif-icon-wrap">🔔</div>
            <div class="notif-text">
                <p>Comment from Sara Mahmoud on TCK-2024</p>
                <span class="notif-time">Mon</span>
            </div>
        </div>
    `;

    notifCardBox.innerHTML = htmlContent;
});