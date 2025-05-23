document.getElementById('loginForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value.trim().toLowerCase();
    const password = document.getElementById('password').value;
    
    try {
        const hash = await sha256(password);
        const response = await fetch('/api/auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: email,
                password: hash
            })
        });
        
        const data = await response.json();
        console.log("Auth response:", data);  // Отладочный вывод
        
        if (!response.ok) {
            throw new Error(data.message || 'Ошибка авторизации');
        }
        
        // Сохраняем токен и данные пользователя
        localStorage.setItem('auth_token', data.token);
        localStorage.setItem('user_email', data.email);
        localStorage.setItem('is_admin', data.is_admin);
        
        // Перенаправление с проверкой
        if (data.is_admin) {
            console.log("Redirecting to admin panel");
            window.location.href = "/admin_lk";
        } else {
            console.log("Redirecting to regular LK");
            window.location.href = `/izbr/${data.token}`;
        }
        
    } catch (error) {
        console.error("Login error:", error);
        alert(error.message || 'Ошибка входа');
    }
});