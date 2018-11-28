$files = Get-ChildItem -Path ./ -File | Where-Object {-not $_.Name.EndsWith(".ps1")}

cd ..

foreach ($file in $files) {
    Write-Output $(Get-Content ".\demo\$($file)")
    Pause
    Get-Content ".\demo\$($file)" | python.exe .\derp.py
    Pause
    Clear-Host
}