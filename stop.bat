@echo off
echo Stopping Job Similarity Application...
docker-compose down

echo.
set /p REMOVE_VOLUMES="Do you want to remove volumes? (y/N) "
if /i "%REMOVE_VOLUMES%"=="y" (
    docker-compose down -v
    echo Volumes removed.
)

echo Application stopped.
pause