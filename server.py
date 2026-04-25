from http.server import HTTPServer, BaseHTTPRequestHandler

count = 0

class CounterHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        html = f"""
        <html>
            <body style="text-align: center; padding-top: 50px; font-family: sans-serif;">
                <h1>Counter</h1>
                <div style="font-size: 48px; margin: 20px;">{count}</div>
                <form method="POST">
                    <button type="submit" style="padding: 15px 30px; font-size: 20px; cursor: pointer;">add 1</button>
                </form>
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

print("伺服器已啟動：http://192.168.50.8:8000")
HTTPServer(('0.0.0.0', 8000), CounterHandler).serve_forever()
