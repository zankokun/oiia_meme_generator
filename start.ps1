#!/usr/bin/env pwsh
$ErrorActionPreference = "Stop"

Write-Host "OIIA Cat Meme Generator" -ForegroundColor Cyan

if (-not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    npm install
}

$port = 3000
$existing = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "Port $port in use, killing existing process..." -ForegroundColor Yellow
    $existing | Select-Object OwningProcess -Unique | ForEach-Object {
        Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
    }
    Start-Sleep -Seconds 1
}

Write-Host "Starting server on http://localhost:$port" -ForegroundColor Green
node server.js
