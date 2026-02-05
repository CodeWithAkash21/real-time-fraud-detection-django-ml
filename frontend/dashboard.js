const API_BASE = '/api';

document.addEventListener('DOMContentLoaded', () => {
    fetchStats();
    fetchTransactions();
});

async function fetchStats() {
    try {
        const res = await fetch(`${API_BASE}/stats/`);
        const data = await res.json();

        document.getElementById('kpi-total').innerText = data.total_transactions.toLocaleString();
        document.getElementById('kpi-fraud').innerText = data.fraud_transactions.toLocaleString();
        document.getElementById('kpi-rate').innerText = data.fraud_rate + '%';

        initCharts(data);
    } catch (err) {
        console.error("Error fetching stats:", err);
    }
}

async function fetchTransactions() {
    try {
        const tbody = document.getElementById('tx-table-body');
        tbody.innerHTML = '<tr><td colspan="5" class="px-6 py-4 text-center text-gray-500">Refreshing...</td></tr>';

        const res = await fetch(`${API_BASE}/transactions/`);
        const data = await res.json();

        tbody.innerHTML = '';

        if (data.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="px-6 py-4 text-center text-gray-500">No recent transactions</td></tr>';
            return;
        }

        data.forEach(tx => {
            const date = new Date(tx.created_at).toLocaleString();
            const isFraud = tx.is_fraud;
            const statusClass = isFraud ? 'text-red-500 bg-red-900/20 px-2 py-1 rounded' : 'text-green-500 bg-green-900/20 px-2 py-1 rounded';
            const statusText = isFraud ? 'FRAUD' : 'LEGIT';

            const tr = `
                <tr>
                    <td>${tx.transaction_id}</td>
                    <td>$${tx.amount.toFixed(2)}</td>
                    <td>${date}</td>
                    <td><span style="font-family: monospace; color: #64748b;">[${tx.features.slice(0, 3).join(', ')}...]</span></td>
                    <td style="font-weight: bold;">${(tx.fraud_probability * 100).toFixed(2)}%</td>
                    <td>
                        <span class="${statusClass}" style="padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: 700; background: ${isFraud ? 'rgba(239, 68, 68, 0.2)' : 'rgba(16, 185, 129, 0.2)'}; color: ${isFraud ? '#ef4444' : '#10b981'};">
                            ${statusText}
                        </span>
                    </td>
                </tr>
            `;
            tbody.innerHTML += tr;
        });
    } catch (err) {
        console.error("Error fetching transactions:", err);
        document.getElementById('tx-table-body').innerHTML = '<tr><td colspan="6" style="text-align: center; color: #ef4444;">Error loading data</td></tr>';
    }
}

function initCharts(data) {
    // Simple mock charts for now as api/stats might need more detailed time-series data
    // We will just show distribution

    const ctxFraud = document.getElementById('fraudChart').getContext('2d');
    new Chart(ctxFraud, {
        type: 'doughnut',
        data: {
            labels: ['Legit', 'Fraud'],
            datasets: [{
                data: [data.total_transactions - data.fraud_transactions, data.fraud_transactions],
                backgroundColor: ['#10B981', '#EF4444'],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '80%',
            plugins: {
                legend: { display: false }
            }
        }
    });

    const ctxVol = document.getElementById('volumeChart').getContext('2d');
    const gradient = ctxVol.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(59, 130, 246, 0.5)');
    gradient.addColorStop(1, 'rgba(59, 130, 246, 0)');

    new Chart(ctxVol, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Transactions',
                data: [120, 190, 300, 250, 200, 180, 220],
                borderColor: '#3b82f6',
                backgroundColor: gradient,
                borderWidth: 2,
                pointBackgroundColor: '#3b82f6',
                pointBorderColor: '#0f172a',
                pointBorderWidth: 2,
                pointRadius: 4,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    grid: { color: '#1e293b' },
                    ticks: { color: '#64748b', font: { family: 'Inter' } },
                    border: { display: false }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#64748b', font: { family: 'Inter' } },
                    border: { display: false }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1e293b',
                    titleColor: '#e2e8f0',
                    bodyColor: '#94a3b8',
                    padding: 12,
                    borderColor: '#334155',
                    borderWidth: 1,
                    displayColors: false
                }
            }
        }
    });
}
