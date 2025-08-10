document.addEventListener("DOMContentLoaded", function() {
    const drawer = document.getElementById('drawer');
    const menuBtn = document.getElementById('menuBtn');
    const body = document.body;
    const dayBtn = document.getElementById('dayModeBtn');
    const nightBtn = document.getElementById('nightModeBtn');

    // باز و بسته کردن منو
    menuBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        drawer.classList.toggle('open');
        body.classList.toggle('drawer-open', drawer.classList.contains('open'));
    });

    document.addEventListener('click', function(e) {
        if (!drawer.contains(e.target) && !menuBtn.contains(e.target)) {
            drawer.classList.remove('open');
            body.classList.remove('drawer-open');
        }
    });

    // حالت روز
    dayBtn.addEventListener('click', function() {
        body.classList.remove('night');
        body.classList.add('day');
        localStorage.setItem("theme", "day");
    });

    // حالت شب
    nightBtn.addEventListener('click', function() {
        body.classList.remove('day');
        body.classList.add('night');
        localStorage.setItem("theme", "night");
    });

    // لود تم از حافظه
    const savedTheme = localStorage.getItem("theme");
    if (savedTheme) {
        body.classList.remove('day', 'night');
        body.classList.add(savedTheme);
    }
});
