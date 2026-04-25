from http.server import HTTPServer, BaseHTTPRequestHandler

count = 0

class CounterHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # 這裡加入了 CSS 樣式
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
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Counter</h1>
                    <div class="number">{count}</div>
                    <form method="POST">
                        <button type="submit">Count + 1</button>
                    </form>
                </div>
            </body>
        </html>
        """
        self.wfile.write(html.encode())

    def do_POST(self):
        global count
        count += 1
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()

print("伺服器已啟動：http://0.0.0.0:8000")
HTTPServer(('0.0.0.0', 8000), CounterHandler).serve_forever()