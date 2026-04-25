from http.server import HTTPServer, BaseHTTPRequestHandler
import json

count = 0


class CounterHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # API endpoint to get current count
        if self.path == '/api/count':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({'count': count}).encode())
            return

        # Serve the main HTML page
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>SNAS Counter</title>
                <style>
                    :root {{
                        --bg: #f0f2f5;
                        --card: #ffffff;
                        --text: #1c1e21;
                        --primary: #007bff;
                        --primary-hover: #0056b3;
                    }}
                    @media (prefers-color-scheme: dark) {{
                        :root {{
                            --bg: #18191a;
                            --card: #242526;
                            --text: #e4e6eb;
                        }}
                    }}
                    body {{
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        min-height: 100vh;
                        margin: 0;
                        background-color: var(--bg);
                        color: var(--text);
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                    }}
                    .container {{
                        background: var(--card);
                        padding: 2rem;
                        border-radius: 16px;
                        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                        text-align: center;
                        width: 90%;
                        max-width: 320px;
                    }}
                    h1 {{ margin-top: 0; font-size: 1.2rem; opacity: 0.8; }}
                    .number {{
                        font-size: 4rem;
                        font-weight: bold;
                        margin: 1.5rem 0;
                        color: var(--primary);
                    }}
                    button {{
                        background-color: var(--primary);
                        color: white;
                        border: none;
                        padding: 12px 24px;
                        font-size: 1.1rem;
                        border-radius: 8px;
                        cursor: pointer;
                        width: 100%;
                        transition: background 0.2s, transform 0.1s;
                    }}
                    button:hover {{ background-color: var(--primary-hover); }}
                    button:active {{ transform: scale(0.98); }}
                    .row {{ display: flex; gap: 0.5rem; }}
                    .row button {{ width: 50%; padding: 10px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Counter</h1>
                    <div id="number" class="number">{count}</div>
                    <div class="row">
                        <form id="manualForm" method="POST" style="width:50%; margin:0;">
                            <button type="submit">+1</button>
                        </form>
                        <button id="autoBtn" style="width:50%;">Auto: Off</button>
                    </div>
                </div>

                <script>
                    let autoOn = false;
                    let autoTimer = null;

                    async function fetchCount() {
                        try {
                            const res = await fetch('/api/count');
                            if (res.ok) {
                                const data = await res.json();
                                document.getElementById('number').textContent = data.count;
                            }
                        } catch (e) { console.error(e); }
                    }

                    async function incOnce() {
                        try {
                            const res = await fetch('/inc', {method: 'POST'});
                            if (res.ok) {
                                const data = await res.json();
                                document.getElementById('number').textContent = data.count;
                            }
                        } catch (e) { console.error(e); }
                    }

                    document.getElementById('manualForm').addEventListener('submit', async (e) => {
                        e.preventDefault();
                        await incOnce();
                    });

                    document.getElementById('autoBtn').addEventListener('click', () => {
                        autoOn = !autoOn;
                        const btn = document.getElementById('autoBtn');
                        btn.textContent = autoOn ? 'Auto: On' : 'Auto: Off';
                        if (autoOn) {
                            // do one immediately then start interval
                            incOnce();
                            autoTimer = setInterval(incOnce, 1000);
                        } else {
                            clearInterval(autoTimer);
                            autoTimer = null;
                        }
                    });

                    // keep UI in sync
                    setInterval(fetchCount, 1500);
                    fetchCount();
                </script>
            </body>
        </html>
        """
        self.wfile.write(html.encode())

    def do_POST(self):
        global count
        # AJAX increment endpoint
        if self.path == '/inc':
            count += 1
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({'count': count}).encode())
            return

        # fallback: treat other POSTs as manual increment then redirect
        count += 1
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()


print("伺服器已啟動：http://0.0.0.0:8000")
HTTPServer(('0.0.0.0', 8000), CounterHandler).serve_forever()