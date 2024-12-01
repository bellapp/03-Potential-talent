batch
@echo off
echo Starting services...
docker-compose up -d

echo Waiting for Ollama to start...
:WAIT_OLLAMA
timeout /t 5 /nobreak > nul
curl -s http://localhost:11434/api/version
if errorlevel 1 (
    echo Waiting for Ollama...
    goto WAIT_OLLAMA
)

echo Ollama is ready! Pulling Mistral model...
curl -X POST http://localhost:11434/api/pull -H "Content-Type: application/json" -d "{\"name\":\"mistral:instruct\"}"

echo.
echo All services are ready!
echo Access the application at http://localhost:8501
echo.
echo Showing logs (Ctrl+C to exit)...
docker-compose logs -f