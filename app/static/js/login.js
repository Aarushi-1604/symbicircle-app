document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // OAuth2PasswordRequestForm expects URL-encoded parameters
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });

        if (response.ok) {
            const data = await response.json();

            // Save the JWT token to LocalStorage
            localStorage.setItem('token', data.access_token);

            // Redirect to the Home Page
            window.location.href = "/";
        } else {
            const error = await response.json();
            alert(error.detail || "Invalid email or password.");
        }
    } catch (err) {
        console.error("Login Error:", err);
        alert("Server connection failed.");
    }
});