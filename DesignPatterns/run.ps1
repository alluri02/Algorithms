# Design Patterns Project Build and Run Script

Write-Host "=== Design Patterns Project ===" -ForegroundColor Green
Write-Host "Compiling Java source files..." -ForegroundColor Yellow

# Change to script directory
Set-Location $PSScriptRoot

# Create target directory if it doesn't exist
if (!(Test-Path "target\classes")) {
    New-Item -ItemType Directory -Path "target\classes" -Force | Out-Null
}

# Compile all Java files
$javaFiles = Get-ChildItem -Recurse -Filter "*.java" "src\main\java"
foreach ($file in $javaFiles) {
    Write-Host "Compiling: $($file.Name)" -ForegroundColor Cyan
    javac -d "target\classes" -cp "src\main\java" $file.FullName
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Compilation failed for $($file.Name)" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Compilation completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Running Design Patterns Demo..." -ForegroundColor Yellow
Write-Host "================================" -ForegroundColor Yellow

# Run the main class
java -cp "target\classes" com.example.patterns.Main

Write-Host ""
Write-Host "Demo completed!" -ForegroundColor Green
