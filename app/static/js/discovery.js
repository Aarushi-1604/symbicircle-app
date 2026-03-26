// 1. Auth Guard
if (!localStorage.getItem('token')) {
    window.location.href = "/login";
}

// 2. Initial Page Setup
document.addEventListener('DOMContentLoaded', () => {
    // Fetch user details for the greeting (Top Right)
    fetchUserProfile();

    // Initial load of students
    fetchUsers();

    // 3. EVENT LISTENERS
    // Magnifying Glass Button Click

    const searchBtn = document.getElementById('searchBtn');
    if (searchBtn) {
        searchBtn.onclick = () => {
            console.log("Search button clicked!"); // Debug to see if it triggers
            fetchUsers();
        };
    }

    // "Enter" key in search input
    const skillSearch = document.getElementById('skillSearch');
    skillSearch.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            fetchUsers();
        }
    });

    // Optional: Search as you type (with a tiny delay to save server resources)
    let timeout = null;
    skillSearch.addEventListener('input', () => {
        clearTimeout(timeout);
        timeout = setTimeout(fetchUsers, 500);
    });
});

async function fetchUserProfile() {
    try {
        const response = await fetch('/auth/me', {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        if (response.ok) {
            const user = await response.json();
            document.getElementById('userGreeting').textContent = `Hi, ${user.full_name.split(' ')[0]}!`;
        }
    } catch (err) {
        console.error("Profile fetch failed");
    }
}

async function fetchUsers() {
    const branchElement = document.querySelector('input[name="branch"]:checked');
    const branch = branchElement ? branchElement.value : "";
    const skills = document.getElementById('skillSearch').value.trim();

    // Build query params properly to avoid "?" vs "&" mess
    const params = new URLSearchParams();
    if (branch) params.append('branch', branch);
    if (skills) params.append('skill_query', skills);

    try {
        const response = await fetch(`/users/search?${params.toString()}`);
        const users = await response.json();
        renderUsers(users);
    } catch (err) {
        console.error("Search failed:", err);
    }
}

function renderUsers(users) {
    const grid = document.getElementById('userGrid');

    if (!users || users.length === 0) {
        grid.innerHTML = `
            <div class="col-span-full text-center py-12">
                <p class="text-slate-400 italic">No one in the circle matches those filters...</p>
            </div>`;
        return;
    }

    grid.innerHTML = '';
    users.forEach(user => {
        const card = document.createElement('div');
        card.className = "glass p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all border-white/50 flex flex-col justify-between";

        const skillPills = user.skills.map(s =>
            `<span class="bg-blue-100 text-blue-700 text-[10px] px-2 py-1 rounded-md font-bold uppercase tracking-wider">${s.name}</span>`
        ).join('');

        card.innerHTML = `
            <div>
                <div class="flex justify-between items-start mb-4">
                    <div>
                        <h4 class="font-bold text-lg text-slate-800">${user.full_name}</h4>
                        <p class="text-xs text-slate-500 font-medium uppercase">${user.branch} | Batch ${user.batch}</p>
                    </div>
                    <div class="bg-blue-50 text-blue-600 px-2 py-1 rounded-lg text-[10px] font-black border border-blue-100">SIT</div>
                </div>
                <div class="flex flex-wrap gap-2 mt-4">
                    ${skillPills}
                </div>
            </div>
            <button onclick="connectWithUser(${user.id})" class="w-full mt-6 py-2 bg-slate-800 text-white rounded-xl text-sm font-semibold hover:bg-blue-600 transition shadow-md active:scale-95">
                Connect
            </button>
        `;
        grid.appendChild(card);
    });
}

function logout() {
    localStorage.removeItem('token');
    window.location.href = "/login";
}

// Placeholder for next feature
function connectWithUser(userId) {
    console.log(`Sending request to user ID: ${userId}`);
    alert("Connect feature coming soon!");
}