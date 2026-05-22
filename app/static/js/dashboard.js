let completionChart = null;
let statusChart = null;

const demoTasks = [
    { title: "Prepare sprint report", status: "in_progress", priority: "high", due_date: new Date().toISOString() },
    { title: "Review blocked tasks", status: "pending", priority: "medium", due_date: null },
    { title: "Publish analytics export", status: "completed", priority: "low", due_date: new Date().toISOString() },
];

const demoStats = {
    total_tasks: 24,
    completed_tasks: 17,
    completion_rate: 70.8,
    status_distribution: {
        completed: 17,
        in_progress: 4,
        pending: 3,
    },
};

const demoProductivity = {
    productivity_trend: [64, 68, 71, 76],
    daily_metrics: [
        { date: "Mon", completed: 3 },
        { date: "Tue", completed: 5 },
        { date: "Wed", completed: 4 },
        { date: "Thu", completed: 6 },
        { date: "Fri", completed: 7 },
    ],
};

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("refreshDashboard")?.addEventListener("click", loadDashboard);
    loadDashboard();
});

async function loadDashboard() {
    clearNotice();
    const token = getAccessToken();

    if (!token) {
        renderPreviewState();
        return;
    }

    try {
        const [tasks, stats, productivity] = await Promise.all([
            fetchJson("/api/v1/tasks/", token),
            fetchJson("/api/v1/analytics/tasks/statistics", token),
            fetchJson("/api/v1/analytics/productivity", token),
        ]);

        renderTasks(tasks);
        renderAnalytics(stats);
        renderProductivity(productivity);
        renderStatusChart(stats.status_distribution);
    } catch (error) {
        renderPreviewState("Unable to load protected workspace metrics. Showing preview data instead.");
    }
}

async function fetchJson(url, token) {
    const response = await fetch(url, {
        headers: {
            Authorization: `Bearer ${token}`,
        },
    });
    if (!response.ok) {
        throw new Error(`Request failed: ${response.status}`);
    }
    return response.json();
}

function getAccessToken() {
    return localStorage.getItem("taskflow_access_token") || localStorage.getItem("access_token") || "";
}

function renderPreviewState(message = "Preview mode is active. Add an access token to localStorage to load protected workspace metrics.") {
    showNotice(message);
    renderTasks(demoTasks);
    renderAnalytics(demoStats);
    renderProductivity(demoProductivity);
    renderStatusChart(demoStats.status_distribution);
}

function showNotice(message) {
    const notice = document.getElementById("dashboardNotice");
    if (!notice) return;
    notice.textContent = message;
    notice.classList.remove("is-hidden");
}

function clearNotice() {
    const notice = document.getElementById("dashboardNotice");
    if (!notice) return;
    notice.textContent = "";
    notice.classList.add("is-hidden");
}

function renderTasks(tasks) {
    const container = document.getElementById("recentTasks");
    if (!container) return;

    if (!Array.isArray(tasks) || tasks.length === 0) {
        container.innerHTML = `<tr><td colspan="4" class="empty-cell">No tasks found for this workspace.</td></tr>`;
        return;
    }

    container.innerHTML = "";
    tasks.slice(0, 8).forEach(task => {
        const dueDate = task.due_date ? new Date(task.due_date).toLocaleDateString() : "No due date";
        const row = document.createElement("tr");
        row.innerHTML = `
            <td><strong>${escapeHtml(task.title || "Untitled task")}</strong></td>
            <td>${badge(task.status || "pending", "status")}</td>
            <td>${badge(task.priority || "medium", "priority")}</td>
            <td>${escapeHtml(dueDate)}</td>
        `;
        container.appendChild(row);
    });
}

function renderAnalytics(stats) {
    setText("totalTasks", stats.total_tasks || 0);
    setText("completedTasks", stats.completed_tasks || 0);
    setText("completionRate", `${formatNumber(stats.completion_rate || 0)}%`);
    setText("productivityScore", stats.avg_estimation_accuracy_percent ? formatNumber(stats.avg_estimation_accuracy_percent) : "0");
}

function renderProductivity(productivity) {
    const trend = Array.isArray(productivity.productivity_trend) ? productivity.productivity_trend : [];
    const score = trend.length > 0 ? trend[trend.length - 1] : 0;
    setText("productivityScore", formatNumber(score));

    const dailyMetrics = Array.isArray(productivity.daily_metrics) ? productivity.daily_metrics : [];
    const labels = dailyMetrics.map(item => item.date);
    const completedData = dailyMetrics.map(item => item.completed);

    renderLineChart(labels, completedData);
}

function renderLineChart(labels, completedData) {
    const canvas = document.getElementById("completionTrend");
    if (!canvas) return;
    if (typeof Chart === "undefined") {
        renderChartFallback(canvas, "Chart library unavailable.");
        return;
    }

    const ctx = canvas.getContext("2d");
    if (completionChart) {
        completionChart.destroy();
    }

    completionChart = new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [
                {
                    label: "Completed Tasks",
                    data: completedData,
                    borderColor: "#1f6f8b",
                    backgroundColor: "rgba(31, 111, 139, 0.12)",
                    pointBackgroundColor: "#164e63",
                    pointRadius: 4,
                    fill: true,
                    tension: 0.35,
                },
            ],
        },
        options: chartOptions(),
    });
}

function renderStatusChart(statusDistribution) {
    const canvas = document.getElementById("statusDistribution");
    if (!canvas) return;
    if (typeof Chart === "undefined") {
        renderChartFallback(canvas, "Chart library unavailable.");
        return;
    }

    const labels = Object.keys(statusDistribution || {});
    const values = Object.values(statusDistribution || {});
    const ctx = canvas.getContext("2d");

    if (statusChart) {
        statusChart.destroy();
    }

    statusChart = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels,
            datasets: [{
                data: values,
                backgroundColor: ["#16855f", "#1f6f8b", "#a05f00", "#b42318", "#667385"],
                borderColor: "#ffffff",
                borderWidth: 4,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: "bottom",
                    labels: {
                        boxWidth: 12,
                        color: "#667385",
                        font: { weight: "700" },
                    },
                },
            },
        },
    });
}

function chartOptions() {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
        },
        scales: {
            x: {
                ticks: { color: "#667385", font: { weight: "700" } },
                grid: { display: false },
            },
            y: {
                beginAtZero: true,
                ticks: { color: "#667385" },
                grid: { color: "#eef2f6" },
            },
        },
    };
}

function renderChartFallback(canvas, message) {
    const frame = canvas.closest(".chart-frame");
    if (!frame) return;
    frame.innerHTML = `<div class="chart-fallback">${escapeHtml(message)}</div>`;
}

function badge(value, type) {
    const normalized = String(value).toLowerCase().replaceAll("_", "-");
    return `<span class="badge ${type}-${normalized}">${escapeHtml(String(value).replaceAll("_", " "))}</span>`;
}

function setText(id, value) {
    const element = document.getElementById(id);
    if (element) {
        element.textContent = value;
    }
}

function formatNumber(value) {
    return Math.round(Number(value || 0) * 10) / 10;
}

function escapeHtml(value) {
    const div = document.createElement("div");
    div.textContent = value;
    return div.innerHTML;
}
