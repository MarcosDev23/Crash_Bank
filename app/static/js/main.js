function toggleTheme() {
    const body = document.body;
    // Alterna a classe light-mode no body
    body.classList.toggle('light-mode');

    // Salva a preferência do usuário
    if (body.classList.contains('light-mode')) {
        localStorage.setItem('theme', 'light');
    } else {
        localStorage.setItem('theme', 'dark');
    }
}

// Verifica o tema salvo ao carregar a página
window.onload = () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
    }
};


