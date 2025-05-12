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
        alert('Регистрация успешна!');
        let hash = await sha256(password);
        window.fetch("http://127.0.0.1:5000").then(function(response) { 
            alert(response.text());
        });
        // window.location.href = 'profile.html';
        let request_body = {"full_name": fullName, "email": email, "password": hash};
        const request_properties = {
            method : 'POST',
            headers : {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body : JSON.stringify(request_body)
        }
        
        const response = await window.fetch("http://127.0.0.1:5000/api/register", request_properties)
        .then((response) => { 
            response.json().then(res => console.log(res));
            window.location.href = 'izbr.html'; // Перенаправление после успешного входа
        })
        .catch((err) => console.error(err));
    }
});