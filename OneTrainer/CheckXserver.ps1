# Script to check X server installation on Windows 11
# Save this file as CheckXserver.ps1 and run through PowerShell

# Array of X servers to look for
$xServers = @(
    @{Name = "VcXsrv"; ExeName = "vcxsrv.exe"; InstallDir = "VcXsrv"},
    @{Name = "Xming"; ExeName = "Xming.exe"; InstallDir = "Xming"},
    @{Name = "MobaXterm"; ExeName = "MobaXterm.exe"; InstallDir = "MobaXterm"},
    @{Name = "X410"; ExeName = "X410.exe"; InstallDir = "X410"},
    @{Name = "Cygwin/X"; ExeName = "XWin.exe"; InstallDir = "Cygwin"}
)

Write-Host "Checking for installed X servers on Windows 11..." -ForegroundColor Cyan
Write-Host "-------------------------------------------------" -ForegroundColor Cyan

$foundAny = $false

# Check installed programs through registry
Write-Host "1. Checking installed programs list:" -ForegroundColor Yellow
$installedPrograms = @()
$installedPrograms += Get-ItemProperty "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*"
$installedPrograms += Get-ItemProperty "HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*"
try {
    $installedPrograms += Get-ItemProperty "HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*"
} catch {
    # 32-bit registry might not exist
}

foreach ($server in $xServers) {
    $found = $installedPrograms | Where-Object { $_.DisplayName -like "*$($server.Name)*" }
    if ($found) {
        Write-Host "  [INSTALLED] $($server.Name)" -ForegroundColor Green
        Write-Host "    Path: $($found.InstallLocation)" -ForegroundColor Gray
        $foundAny = $true
    }
}

if (-not $foundAny) {
    Write-Host "  No X servers found in registry." -ForegroundColor Gray
}
$foundAny = $false

# Check running processes
Write-Host "`n2. Checking running processes:" -ForegroundColor Yellow
foreach ($server in $xServers) {
    $processName = $server.ExeName.Replace(".exe", "")
    $process = Get-Process -Name $processName -ErrorAction SilentlyContinue
    if ($process) {
        Write-Host "  [RUNNING] $($server.Name)" -ForegroundColor Green
        Write-Host "    Process ID: $($process.Id)" -ForegroundColor Gray
        $foundAny = $true
    }
}

if (-not $foundAny) {
    Write-Host "  No running X servers detected." -ForegroundColor Gray
}
$foundAny = $false

# Check standard installation directories
Write-Host "`n3. Checking files in standard directories:" -ForegroundColor Yellow
$programFiles = @(
    ${env:ProgramFiles},
    ${env:ProgramFiles(x86)},
    "$env:LOCALAPPDATA\Programs"
)

foreach ($dir in $programFiles) {
    if (Test-Path $dir) {
        foreach ($server in $xServers) {
            $paths = @(
                "$dir\$($server.InstallDir)\$($server.ExeName)",
                "$dir\$($server.ExeName)"
            )

            foreach ($path in $paths) {
                if (Test-Path $path) {
                    Write-Host "  [FOUND] $($server.Name)" -ForegroundColor Green
                    Write-Host "    Path: $path" -ForegroundColor Gray
                    $foundAny = $true
                }
            }
        }
    }
}

# Check Microsoft Store apps
Write-Host "`n4. Checking Microsoft Store apps:" -ForegroundColor Yellow
try {
    $storeApps = Get-AppxPackage | Where-Object { $_.Name -like "*X410*" }
    if ($storeApps) {
        Write-Host "  [INSTALLED] X410 (Microsoft Store)" -ForegroundColor Green
        Write-Host "    Version: $($storeApps.Version)" -ForegroundColor Gray
        $foundAny = $true
    }
} catch {
    Write-Host "  Unable to check Microsoft Store apps." -ForegroundColor Gray
}

if (-not $foundAny) {
    Write-Host "  No X servers found in standard directories." -ForegroundColor Gray
}

Write-Host "`nCheck completed." -ForegroundColor Cyan
Write-Host "If no X server was found, it's recommended to install VcXsrv:" -ForegroundColor Cyan
Write-Host "https://sourceforge.net/projects/vcxsrv/" -ForegroundColor White