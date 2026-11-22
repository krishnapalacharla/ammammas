# Encode generated originals for the storefront. No crop, resize or retouching.
Add-Type -AssemblyName System.Drawing
$studioProjectRoot = Split-Path -Parent $PSScriptRoot
$studioOriginals = Join-Path $studioProjectRoot 'brand-assets/studio-originals'
$studioAssets = Join-Path $studioProjectRoot 'theme/assets'
$studioEncoder = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object MimeType -eq 'image/jpeg'
$studioQuality = New-Object System.Drawing.Imaging.EncoderParameters(1)
$studioQuality.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]93)
$studioReport = @()
try {
    Get-ChildItem -LiteralPath $studioOriginals -Filter 'studio-*.png' | ForEach-Object {
        $studioImage = [System.Drawing.Image]::FromFile($_.FullName)
        try {
            $studioTarget = Join-Path $studioAssets ($_.BaseName + '.jpg')
            $studioImage.Save($studioTarget, $studioEncoder, $studioQuality)
            $studioReport += [PSCustomObject]@{ asset = $_.BaseName + '.jpg'; width = $studioImage.Width; height = $studioImage.Height; bytes = (Get-Item -LiteralPath $studioTarget).Length }
        } finally { $studioImage.Dispose() }
    }
} finally { $studioQuality.Dispose() }
$studioReport | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $studioProjectRoot 'docs/studio-image-assets.json') -Encoding utf8
$studioReport | Format-Table
