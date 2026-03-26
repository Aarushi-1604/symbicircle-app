document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const emailInput = document.getElementById('email');
    const emailStatus = document.getElementById('emailStatus');

    // SIT Email Validation Logic
    emailInput.addEventListener('input', () => {
        const email = emailInput.value.toLowerCase();
        if (email.length > 0) {
            emailStatus.classList.remove('hidden');
            if (email.endsWith('@sitpune.edu.in')) {
                emailStatus.textContent = "✅ Valid SIT Pune email";
                emailStatus.className = "mt-1 text-xs text-green-600 font-medium";
            } else {
                emailStatus.textContent = "❌ Must end with @sitpune.edu.in";
                emailStatus.className = "mt-1 text-xs text-red-500 font-medium";
            }
        } else {
            emailStatus.classList.add('hidden');
        }
    });

    registerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const email = emailInput.value.toLowerCase();
        if (!email.endsWith('@sitpune.edu.in')) {
            alert("Please use your official SIT Pune email address.");
            return;
        }

        // Collect data for Step 2 (Skill Selection)
        const userData = {
            full_name: document.getElementById('fullName').value,
            email: email,
            password: document.getElementById('password').value,
            branch: document.getElementById('branch').value,
            batch: document.getElementById('batch').value
        };

        // Temporarily store in sessionStorage to carry to Step 2
        sessionStorage.setItem('tempUser', JSON.stringify(userData));

        // Redirect to Step 2 (The Skill Bubbles page)
        window.location.href = "/register/skills";
    });
});