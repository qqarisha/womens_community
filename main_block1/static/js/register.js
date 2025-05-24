async function sha256(str) {
    const buf = new TextEncoder().encode(str);
    const digest = await crypto.subtle.digest('SHA-256', buf);
    return Array.from(new Uint8Array(digest))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');
}

document.getElementById('registrationForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Сброс сообщений об ошибках
    document.querySelectorAll('.error-message').forEach(el => {
        el.style.display = 'none';
    });
    
    // Валидация
    let isValid = true;
    const fullName = document.getElementById('fullName').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (fullName.length < 3) {
        document.getElementById('fullNameError').textContent = 'Введите полное имя';
        document.getElementById('fullNameError').style.display = 'block';
        isValid = false;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        document.getElementById('emailError').textContent = 'Введите корректный email';
        document.getElementById('emailError').style.display = 'block';
        isValid = false;
    }
    
    if (password.length < 6) {
        document.getElementById('passwordError').textContent = 'Пароль должен содержать минимум 6 символов';
        document.getElementById('passwordError').style.display = 'block';
        isValid = false;
    }
    
    if (password !== confirmPassword) {
        document.getElementById('confirmPasswordError').textContent = 'Пароли не совпадают';
        document.getElementById('confirmPasswordError').style.display = 'block';
        isValid = false;
    }
    
    if (isValid) {
        let hash = await sha256(password);

        let request_body = {"full_name": fullName, "email": email, "password": hash};
        const request_properties = {
            method : 'POST',
            headers : {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body : JSON.stringify(request_body)
        }
        
        try {
            const response = await window.fetch("http://127.0.0.1:5000/api/register", request_properties);
            const data = await response.json();
            
            if (data.status === 200) {
                // После регистрации выполняем авторизацию для получения токена
                const authResponse = await window.fetch("http://127.0.0.1:5000/api/auth", request_properties);
                const authData = await authResponse.json();
                
                if (authData.status === 200) {
                    window.location.href = `lk/izbr/${authData.token}`;
                    alert('Регистрация успешна!');
                } else {
                    window.location.href = 'lk';
                }
            } else {
                console.error('Ошибка авторизации:', data);
                alert('Ошибка входа: ' + data.message);
            }
        } catch (err) {
            console.error('Ошибка сети:', err);
            alert('Ошибка соединения с сервером');
        }
    }
});

document.getElementById('registrationForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Сброс сообщений об ошибках
    document.querySelectorAll('.error-message').forEach(el => {
        el.style.display = 'none';
    });
    
    // Валидация
    let isValid = true;
    const fullName = document.getElementById('fullName').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (fullName.length < 3) {
        document.getElementById('fullNameError').textContent = 'Введите полное имя';
        document.getElementById('fullNameError').style.display = 'block';
        isValid = false;
    }
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        document.getElementById('emailError').textContent = 'Введите корректный email';
        document.getElementById('emailError').style.display = 'block';
        isValid = false;
    }
    
    if (password.length < 6) {
        document.getElementById('passwordError').textContent = 'Пароль должен содержать минимум 6 символов';
        document.getElementById('passwordError').style.display = 'block';
        isValid = false;
    }
    
    if (password !== confirmPassword) {
        document.getElementById('confirmPasswordError').textContent = 'Пароли не совпадают';
        document.getElementById('confirmPasswordError').style.display = 'block';
        isValid = false;
    }
    
    if (isValid) {
        let hash = await sha256(password);

        let request_body = {"full_name": fullName, "email": email, "password": hash};
        const request_properties = {
            method : 'POST',
            headers : {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body : JSON.stringify(request_body)
        }
        
        try {
            const response = await window.fetch("http://127.0.0.1:5000/api/register", request_properties);
            const data = await response.json();
            
            if (data.status === 200) {
                // После регистрации выполняем авторизацию для получения токена
                const authResponse = await window.fetch("http://127.0.0.1:5000/api/auth", request_properties);
                const authData = await authResponse.json();
                
                if (authData.status === 200) {
                    window.location.href = `lk/izbr/${authData.token}`;
                    alert('Регистрация успешна!');
                } else {
                    window.location.href = 'lk';
                }
            } else {
                console.error('Ошибка авторизации:', data);
                alert('Ошибка входа: ' + data.message);
            }
        } catch (err) {
            console.error('Ошибка сети:', err);
            alert('Ошибка соединения с сервером');
        }
    }
});