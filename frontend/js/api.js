const API_URL = "http://127.0.0.1:8000/api/v1";

async function register(userData) {
    const response = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
    });
    return await response.json();
}

async function login(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
    });
    return await response.json();
}

export { register, login };