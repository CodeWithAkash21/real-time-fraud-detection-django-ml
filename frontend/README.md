# Premium FraudGuard Dashboard

The new dashboard features a high-end FinTech aesthetics built with robust **Vanilla CSS** for maximum performance and stability (no external CDN dependencies).

## Key Features
- **Local FinTech Theme**: Deep dark mode, glassmorphism, and neon accents without unreliable external scripts.
- **Responsive Layout**: Sidebar navigation and CSS Grid data visualization.
- **Interactive Charts**: Gradient-filled Area charts and responsive Doughnut charts.
- **Live Simulation**: A terminal-style interface for transaction testing.

## Setup
1. **Restart Backend**:
   If you haven't already, restart the server to ensure all static files are served correctly:
   ```bash
   python manage.py runserver
   ```

2. **Access**:
   - Go to `http://127.0.0.1:8000/`.
   - It will automatically redirect to the new dashboard at `/static/index.html`.

## Troubleshooting
- **Seeing the old design?**: Clear your browser cache or perform a hard refresh (Ctrl+F5).
- **404 Error?**: Make sure you restarted the server.
