let USER_ID = localStorage.getItem("user_id");

function go(path) {
    window.location.href = path;
}

function logout() {
    localStorage.removeItem("user_id");
    go("/login");
}

function register() {
    fetch("/users/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            name: document.getElementById("name").value,
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        })
    })
    .then(r => r.json())
    .then(d => {
        localStorage.setItem("user_id", d.data.id);
        go("/dashboard");
    });
}

function login() {
    fetch("/users/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            email: document.getElementById("email").value,
            password: document.getElementById("password").value
        })
    })
    .then(r => r.json())
    .then(d => {
        localStorage.setItem("user_id", d.data.id);
        go("/dashboard");
    });
}
async function searchNews() {
    const query = document.getElementById("query").value;
    const chat = document.getElementById("chat");

    if (!query) return;

    chat.innerHTML += `<div class="card">🧑 ${query}</div>`;

    const id = Date.now();
    chat.innerHTML += `<div class="card" id="${id}">🤖 Thinking...</div>`;

    try {
        const res = await fetch("/ai/search", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                query,
                user_id: USER_ID
            })
        });

        const data = await res.json();

        document.getElementById(id).innerHTML =
            `<b>🤖</b> ${data.data.answer}`;

    } catch (err) {
        document.getElementById(id).innerText =
            "❌ Error generating response";
    }
}

async function ingestNews() {
    const status = document.getElementById("status");
    const rss_url = document.getElementById("rss_url").value;

    if (!rss_url) {
        status.innerText = "❌ Please enter RSS URL";
        return;
    }

    status.innerText = "⏳ Fetching news...";

    try {
        const res = await fetch("/ingest", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ rss_url })
        });

        const data = await res.json();

        console.log("INGEST:", data);

        if (data.status === "success") {
            status.innerText =
                `✅ ${data.data.articles_saved} articles ingested`;

            loadNews();
        } else {
            status.innerText = "❌ Failed to ingest";
        }

    } catch (err) {
        console.error(err);
        status.innerText = "❌ Error occurred";
    }
}

async function loadNews() {
    try {
        const res = await fetch("/news?limit=10");
        const data = await res.json();

        const div = document.getElementById("news");
        div.innerHTML = "";

        data.data.forEach(n => {
            div.innerHTML += `
                <div class="news-card">
                    <h4>${n.title}</h4>
                    <p style="font-size:13px; color:#aaa;">
                        ${n.category || "General"}
                    </p>
                    <a href="${n.link}" target="_blank">Read more →</a>
                </div>
            `;
        });

    } catch (err) {
        console.error(err);
    }
}

function addInterest() {
    const keyword = document.getElementById("interest").value;

    if (!USER_ID) {
        alert("User not logged in");
        return;
    }

    if (!keyword) {
        alert("Enter an interest");
        return;
    }

    fetch("/interests", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            user_id: USER_ID,
            interests: [keyword] 
        })
    })
    .then(res => res.json())
    .then(data => {
        console.log("SUCCESS:", data);
        alert("Interest added!");
    })
    .catch(err => console.error(err));
}

async function loadAnalytics() {
    try {
        const res = await fetch("/api/analytics");
        const data = await res.json();

        const categories = data.data.category_distribution;
        const labels = Object.keys(categories);
        const values = Object.values(categories);

        // TOTAL NEWS
        document.getElementById("totalNews").innerText =
            data.data.total_news;

        // BAR CHART
        new Chart(document.getElementById("barChart"), {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "News by Category",
                    data: values
                }]
            }
        });

        // PIE CHART
        new Chart(document.getElementById("pieChart"), {
            type: "pie",
            data: {
                labels: labels,
                datasets: [{
                    data: values
                }]
            }
        });

        // 🔥 LINE CHART (NEW)
        new Chart(document.getElementById("lineChart"), {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "Trend",
                    data: values,
                    fill: false,
                    tension: 0.3
                }]
            }
        });

    } catch (err) {
        console.error(err);
    }
}

if (document.getElementById("barChart")) {
    loadAnalytics();
}