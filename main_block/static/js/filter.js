// Элементы управления
const filterButton = document.querySelector('.main-word-filt');
const filterPage = document.querySelector('.filter-page');
const closeButton = document.querySelector('.close-filter');
const applyButton = document.querySelector('.filter-apply');
const resetButton = document.querySelector('.filter-reset');

// Открытие фильтра
filterButton.addEventListener('click', function () {
    filterPage.style.display = 'flex';
    document.body.style.overflow = 'hidden'; // Блокируем скролл страницы
});

// Закрытие фильтра
closeButton.addEventListener('click', function () {
    filterPage.style.display = 'none';
    document.body.style.overflow = ''; // Восстанавливаем скролл
});

// Применение фильтра
applyButton.addEventListener('click', function () {
    // Здесь код для применения фильтра
    filterPage.style.display = 'none';
    document.body.style.overflow = '';
});

// Сброс фильтра
resetButton.addEventListener('click', function () {
    // Сброс всех выбранных значений
    const inputs = document.querySelectorAll('.filter-page input');
    inputs.forEach(input => {
        input.checked = false;
        if (input.type === 'date') input.value = '';
    });
});

// Закрытие по клику вне области фильтра
filterPage.addEventListener('click', function (e) {
    if (e.target === filterPage) {
        filterPage.style.display = 'none';
        document.body.style.overflow = '';
    }
});