document.addEventListener('DOMContentLoaded', (event) => {
    const appElement = document.querySelector('.tab-content');
    if (appElement) {
        appElement.classList.add('fade-in');
    }
    const filters = document.querySelectorAll('.filters div');
    filters.forEach((filter, index) => {
        filter.style.animationDelay = `${index * 0.1}s`;
        filter.classList.add('fade-in');
    });
});
