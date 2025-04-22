// Элементы управления
const filterButton = document.querySelector('.main-word-filt');
const filterPage = document.querySelector('.filter-page');
const closeButton = document.querySelector('.close-filter');
const applyButton = document.querySelector('.filter-apply');
const resetButton = document.querySelector('.filter-reset');

// Объект для хранения текущих фильтров
const currentFilters = {
    date: null,
    categories: [],
    themes: [],
    locations: []
};

// Открытие фильтра
filterButton.addEventListener('click', () => {
    filterPage.style.display = 'flex';
    document.body.style.overflow = 'hidden';
});

// Закрытие фильтра
const closeFilter = () => {
    filterPage.style.display = 'none';
    document.body.style.overflow = '';
};
closeButton.addEventListener('click', closeFilter);

// Применение фильтра
applyButton.addEventListener('click', () => {
    updateCurrentFilters();
    applyFiltersToContent();
    closeFilter();
    console.log('Applied filters:', currentFilters); // Для отладки
});

// Сброс фильтра
resetButton.addEventListener('click', () => {
    resetAllFilters();
});

// Закрытие по клику вне области
filterPage.addEventListener('click', (e) => {
    if (e.target === filterPage) closeFilter();
});

// Обновление текущих фильтров
function updateCurrentFilters() {
    // Дата
    const dateInput = document.querySelector('.filter-date');
    currentFilters.date = dateInput.value || null;
    
    // Категории
    currentFilters.categories = Array.from(
        document.querySelectorAll('input[name="category"]:checked')
    ).map(el => el.value);
    
    // Тематики
    currentFilters.themes = Array.from(
        document.querySelectorAll('input[name="theme"]:checked')
    ).map(el => el.value);
    
    // Локации
    currentFilters.locations = Array.from(
        document.querySelectorAll('input[name="location"]:checked')
    ).map(el => el.value);
}

// Сброс всех фильтров
function resetAllFilters() {
    // Сброс значений
    document.querySelector('.filter-date').value = '';
    document.querySelectorAll('input[type="checkbox"]').forEach(el => {
        el.checked = false;
    });
    
    // Сброс объекта фильтров
    Object.keys(currentFilters).forEach(key => {
        currentFilters[key] = key === 'date' ? null : [];
    });
    
    // Применение сброса
    applyFiltersToContent();
    console.log('Filters reset');
}

// Применение фильтров к контенту (заглушка - нужно реализовать)
function applyFiltersToContent() {
    // Здесь должна быть логика фильтрации карточек мероприятий
    // На основе currentFilters
    
    // Пример:
    const allCards = document.querySelectorAll('.event-card'); // Предполагаемый класс карточек
    allCards.forEach(card => {
        const meetsCriteria = checkCardAgainstFilters(card);
        card.style.display = meetsCriteria ? 'block' : 'none';
    });
}

// Проверка карточки против фильтров (заглушка)
function checkCardAgainstFilters(card) {
    // Реальная реализация зависит от структуры ваших карточек
    // Это примерный алгоритм:
    
    // 1. Проверка даты
    // 2. Проверка категории
    // 3. Проверка тематики
    // 4. Проверка локации
    
    return true; // Временная заглушка
}

// Инициализация
document.addEventListener('DOMContentLoaded', () => {
    console.log('Filter system initialized');
});