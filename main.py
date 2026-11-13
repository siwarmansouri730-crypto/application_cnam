import http.server
import socketserver
import webbrowser

PORT = 8000

# تشغيل السيرفر المحلي
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Le serveur fonctionne sur: http://localhost:{PORT}")
    # يحل المتصفح تلقائياً على صفحة index.html
    webbrowser.open(f"http://localhost:{PORT}/index.html")
    httpd.serve_forever()