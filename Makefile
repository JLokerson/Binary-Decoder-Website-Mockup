.PHONY: serve serve-python serve-node serve-php help clean open-browser

# Default target - tries Python first, then shows help
serve: serve-python

# Start Python 3 HTTP server on port 8000
serve-python:
	@echo "Starting Python HTTP server on http://localhost:8000"
	@echo "Press Ctrl+C to stop the server"
	@$(MAKE) open-browser &
	@python -m http.server 8000 || python3 -m http.server 8000

# Start Node.js http-server (requires: npm install -g http-server)
serve-node:
	@echo "Starting Node.js HTTP server on http://localhost:8000"
	@echo "Press Ctrl+C to stop the server"
	@$(MAKE) open-browser &
	@npx http-server -p 8000 -c-1

# Start PHP built-in server on port 8000
serve-php:
	@echo "Starting PHP built-in server on http://localhost:8000"
	@echo "Press Ctrl+C to stop the server"
	@$(MAKE) open-browser &
	@php -S localhost:8000

# Open browser (cross-platform)
open-browser:
	@echo "Opening browser..."
	@timeout /t 2 /nobreak >nul 2>&1 || sleep 2 2>/dev/null || ping 127.0.0.1 -n 3 >nul 2>&1
	@start http://localhost:8000 2>/dev/null || open http://localhost:8000 2>/dev/null || xdg-open http://localhost:8000 2>/dev/null || echo "Please manually open http://localhost:8000 in your browser"

# Show available commands
help:
	@echo "Binary Decoder Website - Development Server"
	@echo "==========================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make serve        - Start Python HTTP server (default)"
	@echo "  make serve-python - Start Python HTTP server on port 8000"
	@echo "  make serve-node   - Start Node.js http-server on port 8000"
	@echo "  make serve-php    - Start PHP built-in server on port 8000"
	@echo "  make help         - Show this help message"
	@echo "  make clean        - Clean temporary files"
	@echo ""
	@echo "After starting the server, open http://localhost:8000 in your browser"
	@echo "Note: Camera access requires localhost or HTTPS"

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	@find . -name "*.tmp" -delete 2>/dev/null || true
	@find . -name ".DS_Store" -delete 2>/dev/null || true
	@echo "Clean complete"
