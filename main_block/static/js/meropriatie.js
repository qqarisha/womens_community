    // Получаем модальное окно
    var modal = document.getElementById("registrationModal");

    // Получаем кнопку, которая открывает модальное окно
    var btn = document.querySelector(".register-button");

    // Получаем элемент <span>, который закрывает модальное окно
    var span = document.getElementsByClassName("close")[0];

    // Когда пользователь нажимает на кнопку, открывается модальное окно
    btn.onclick = function() {
        modal.style.display = "block";
    }

    // Когда пользователь нажимает на <span> (x), закрывается модальное окно
    span.onclick = function() {
        modal.style.display = "none";
    }

    // Когда пользователь нажимает в любом месте вне модального окна, оно закрывается
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }