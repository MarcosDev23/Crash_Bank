function toggleTheme() {
    const body = document.body;
    body.classList.toggle('light-mode');

    // Salva a preferência de forma simplificada
    const isLight = body.classList.contains('light-mode');
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
}

(function () {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'light') {
        document.body.classList.add('light-mode');
    }
})();


async function buscarCotacao() {
    const ticker = document.getElementById('tickerInput').value.toUpperCase();
    if (!ticker) return;

    try {
        const response = await fetch(`/get_stock_price?ticker=${ticker}`);
        const data = await response.json();

        if (response.ok) {
            document.getElementById('resultadoInvestimento').style.display = 'block';
            document.getElementById('resTicker').innerText = ticker;
            document.getElementById('resPreco').innerText = `R$ ${data.price.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`;

            // Lógica do Gráfico
            const ctx = document.getElementById('graficoHistorico').getContext('2d');

            // Se já existir um gráfico, destrói para criar o novo
            if (chartInstancia) chartInstancia.destroy();

            chartInstancia = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Preço de Fechamento',
                        data: data.history,
                        borderColor: '#00ff88',
                        backgroundColor: 'rgba(0, 255, 136, 0.1)',
                        fill: true,
                        tension: 0.4, // Curvatura da linha
                        pointRadius: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { grid: { display: false }, ticks: { color: '#888' } },
                        y: { grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: '#888' } }
                    }
                }
            });
        } else {
            alert("Ativo não encontrado.");
        }
    } catch (error) {
        alert("Erro ao buscar dados.");
    }
}