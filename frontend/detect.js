const API_BASE = '/api';

document.getElementById('fill-btn').addEventListener('click', () => {
    // Generate 28 random floats
    const features = Array.from({ length: 28 }, () => (Math.random() * 4 - 2).toFixed(4));
    document.getElementById('features').value = features.join(', ');
    document.getElementById('tx_id').value = 'tx_' + Math.floor(Math.random() * 10000);
    document.getElementById('amount').value = (Math.random() * 1000).toFixed(2);
});

document.getElementById('detect-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const btn = document.getElementById('submit-btn');
    const originalText = btn.innerText;
    btn.innerText = 'Analyzing...';
    btn.disabled = true;

    const txId = document.getElementById('tx_id').value;
    const amount = parseFloat(document.getElementById('amount').value);
    const featureStr = document.getElementById('features').value;

    // Parse features
    // Parse features: split by comma, space, or newline
    const features = featureStr.split(/[\s,]+/).map(s => parseFloat(s.trim())).filter(n => !isNaN(n));

    if (features.length < 28) {
        alert(`Error: Expected at least 28 feature values. Got ${features.length}.`);
        btn.innerText = originalText;
        btn.disabled = false;
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/detect/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                transaction_id: txId,
                amount: amount,
                features: features
            })
        });

        const result = await res.json();

        if (res.ok) {
            showResult(result);
        } else {
            alert('API Error: ' + JSON.stringify(result));
        }

    } catch (err) {
        console.error("Error:", err);
        alert(`Request failed: ${err.message}. Check console for details.`);
    } finally {
        btn.innerText = originalText;
        btn.disabled = false;
    }
});

function showResult(data) {
    const idlePanel = document.getElementById('idle-panel');
    const resultPanel = document.getElementById('result-panel');
    const resultIconBg = document.getElementById('result-icon-bg');

    const scoreVal = document.getElementById('result-score');
    const probBar = document.getElementById('prob-bar');
    const txVal = document.getElementById('res_tx_id');
    const statusVal = document.getElementById('res_status');
    const descVal = document.getElementById('res_desc');
    const icon = document.getElementById('result-icon');

    idlePanel.classList.add('hidden');
    resultPanel.classList.remove('hidden');

    const percentage = (data.fraud_probability * 100).toFixed(2);
    scoreVal.innerText = percentage + '%';
    probBar.style.width = percentage + '%';
    txVal.innerText = data.transaction_id;

    if (data.fraud_detected) {
        // FRAUD CONFIG
        statusVal.innerText = 'FRAUD DETECTED';
        statusVal.style.color = '#ef4444'; // Red
        descVal.innerText = 'Flagged as High Risk Transaction';

        icon.innerText = '⚠️';
        resultIconBg.style.backgroundColor = 'rgba(239, 68, 68, 0.1)';
        resultIconBg.style.color = '#ef4444';
        resultIconBg.style.boxShadow = '0 0 0 4px rgba(239, 68, 68, 0.2)';

        probBar.style.background = '#ef4444';
    } else {
        // LEGIT CONFIG
        statusVal.innerText = 'APPROVED';
        statusVal.style.color = '#10b981'; // Green
        descVal.innerText = 'Transaction appears legitimate';

        icon.innerText = '🛡️';
        resultIconBg.style.backgroundColor = 'rgba(16, 185, 129, 0.1)';
        resultIconBg.style.color = '#10b981';
        resultIconBg.style.boxShadow = '0 0 0 4px rgba(16, 185, 129, 0.2)';

        probBar.style.background = '#10b981';
    }
}
