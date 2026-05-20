document.addEventListener("DOMContentLoaded", () => {
    let reportContainer = document.getElementById("report");
    let issues = JSON.parse(localStorage.getItem("review_report_issues")) || [];
    let score = localStorage.getItem("review_report_score") || 0;

    let reportHTML = `
        <div style="margin-bottom: 20px;">
            <span style="color: #38bdf8; font-weight: 600;">File:</span> code_submission.py
        </div>
        <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 15px;">
    `;

    if (issues.length > 0) {
        reportHTML += `<div style="color: #f87171; font-weight: 600; font-size: 18px; margin-bottom: 15px;">Issues Found:</div>`;
        issues.forEach((issue) => {
            reportHTML += `<div class="issue">${issue}</div>`;
        });
    } else {
        reportHTML += `
            <div class="issue" style="border-left-color: #4caf50;">
                <span class="success">✅ Correct Code! No issues detected.</span>
            </div>
        `;
    }

    reportHTML += `
        </div>
        <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px; display: flex; align-items: center; justify-content: space-between;">
            <div class="score" style="margin-top: 0; font-weight: 600;">Code Quality Score:</div>
            <div style="font-size: 24px; font-weight: 700; color: #38bdf8;">${score} / 10</div>
        </div>
        <div style="display: flex; gap: 15px; margin-top: 25px;">
            <a href="upload_code.html" style="flex: 1;"><button style="margin-top: 0;">Upload Another Code</button></a>
            <a href="dashboard.html" style="flex: 1;"><button style="margin-top: 0;">Back to Dashboard</button></a>
        </div>
    `;

    reportContainer.innerHTML = reportHTML;
});