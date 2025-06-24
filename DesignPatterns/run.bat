@echo off
echo Compiling Design Patterns Project...
cd /d "%~dp0"

:: Create target directory if it doesn't exist
if not exist "target\classes" mkdir "target\classes"

:: Compile all Java files
for /r "src\main\java" %%f in (*.java) do (
    javac -d "target\classes" -cp "src\main\java" "%%f"
)

echo Compilation completed!
echo.
echo Running Design Patterns Demo...
echo.
java -cp "target\classes" com.example.patterns.Main

pause
