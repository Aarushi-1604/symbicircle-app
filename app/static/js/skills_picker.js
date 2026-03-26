document.addEventListener('DOMContentLoaded', () => {
    const skillInput = document.getElementById('skillInput');
    const suggestionsBox = document.getElementById('suggestions');
    const container = document.getElementById('skillsContainer');
    const finishBtn = document.getElementById('finishBtn');

    let selectedSkills = new Set();

    // 1. Fetch suggestions + Handle Custom "Add" Logic
    skillInput.addEventListener('input', async () => {
        const query = skillInput.value.trim();

        if (query.length < 1) {
            suggestionsBox.innerHTML = '';
            suggestionsBox.classList.add('hidden');
            return;
        }

        try {
            // Fetch existing skills from your FastAPI backend
            const res = await fetch(`/users/skills/suggest?q=${query}`);
            const data = await res.json();

            suggestionsBox.innerHTML = '';
            let hasSuggestions = false;

            // A. ALWAYS show the "Add [Typed Text]" option first (LinkedIn style)
            if (!selectedSkills.has(query)) {
                const customDiv = document.createElement('div');
                customDiv.className = "px-4 py-2 bg-blue-50 hover:bg-blue-100 cursor-pointer text-blue-700 font-semibold border-b border-blue-100";
                customDiv.textContent = `Add "${query}"`;
                customDiv.onclick = () => addSkill(query);
                suggestionsBox.appendChild(customDiv);
                hasSuggestions = true;
            }

            // B. Show backend suggestions
            if (data.length > 0) {
                data.forEach(skill => {
                    // Don't show if already selected OR if it exactly matches our 'Custom Add' above
                    if (!selectedSkills.has(skill) && skill.toLowerCase() !== query.toLowerCase()) {
                        const div = document.createElement('div');
                        div.className = "px-4 py-2 hover:bg-slate-50 cursor-pointer text-slate-700 border-b last:border-0";
                        div.textContent = skill;
                        div.onclick = () => addSkill(skill);
                        suggestionsBox.appendChild(div);
                        hasSuggestions = true;
                    }
                });
            }

            // C. Toggle visibility based on if we have ANY options to show
            if (hasSuggestions) {
                suggestionsBox.classList.remove('hidden');
            } else {
                suggestionsBox.classList.add('hidden');
            }

        } catch (err) {
            console.error("Suggestion fetch failed:", err);
        }
    });

    // 2. Add Skill to the Set and UI
    function addSkill(skill) {
        // Clean the skill string (Title Case)
        const cleanSkill = skill.trim();
        if (cleanSkill && !selectedSkills.has(cleanSkill)) {
            selectedSkills.add(cleanSkill);
            renderPills();
        }
        skillInput.value = '';
        suggestionsBox.innerHTML = '';
        suggestionsBox.classList.add('hidden');
        updateButton();
    }

    // 3. Remove Skill
    function removeSkill(skill) {
        selectedSkills.delete(skill);
        renderPills();
        updateButton();
    }

    // 4. Render the Visual Bubbles (Pills)
    function renderPills() {
        container.innerHTML = '';
        selectedSkills.forEach(skill => {
            const pill = document.createElement('div');
            pill.className = "bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-sm font-medium flex items-center gap-2 border border-blue-200 transition-all";
            pill.innerHTML = `
                ${skill} 
                <button class="hover:text-red-500 font-bold focus:outline-none" aria-label="Remove skill">&times;</button>
            `;
            pill.querySelector('button').onclick = () => removeSkill(skill);
            container.appendChild(pill);
        });
    }

    // 5. Update the "Finish" Button State
    function updateButton() {
        const count = selectedSkills.size;
        finishBtn.textContent = `Complete Registration (${count}/5)`;

        if (count >= 5) {
            finishBtn.disabled = false;
            finishBtn.className = "w-full mt-8 bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 rounded-lg shadow-lg cursor-pointer transition transform active:scale-95";
        } else {
            finishBtn.disabled = true;
            finishBtn.className = "w-full mt-8 bg-slate-300 text-white font-bold py-3 rounded-lg cursor-not-allowed transition";
        }
    }

    // 6. Final Submission to Backend
    finishBtn.onclick = async () => {
        // Get user data from Step 1
        const tempUserStr = sessionStorage.getItem('tempUser');
        if (!tempUserStr) {
            alert("Registration data missing. Please start from Step 1.");
            window.location.href = "/register";
            return;
        }

        const userData = JSON.parse(tempUserStr);
        const payload = {
            ...userData,
            skills: Array.from(selectedSkills)
        };

        try {
            const res = await fetch('/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (res.ok) {
                sessionStorage.removeItem('tempUser');
                alert("Welcome to the Circle! Please log in.");
                window.location.href = "/login";
            } else {
                const errorData = await res.json();
                alert(`Error: ${errorData.detail || "Registration failed"}`);
            }
        } catch (err) {
            console.error("Submission error:", err);
            alert("Server connection failed. Please try again.");
        }
    };
});