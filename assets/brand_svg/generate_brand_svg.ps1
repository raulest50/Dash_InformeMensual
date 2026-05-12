Set-StrictMode -Version Latest

Add-Type -AssemblyName PresentationCore
Add-Type -AssemblyName WindowsBase

$OutDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Culture = [Globalization.CultureInfo]::InvariantCulture

function Format-Number {
    param([double]$Value)
    return $Value.ToString("0.###", $Culture)
}

function New-TextPath {
    param(
        [Parameter(Mandatory=$true)][string]$Text,
        [Parameter(Mandatory=$true)][string]$Family,
        [ValidateSet("Normal","Bold","Black","SemiBold","Light")][string]$Weight = "Normal",
        [ValidateSet("Normal","Italic")][string]$Style = "Normal",
        [Parameter(Mandatory=$true)][double]$Size,
        [Parameter(Mandatory=$true)][double]$X,
        [Parameter(Mandatory=$true)][double]$Y,
        [string]$Fill = "#111111",
        [double]$ScaleX = 1.0,
        [double]$ScaleY = 1.0,
        [double]$TargetWidth = 0,
        [string]$Opacity = ""
    )

    $fontFamily = [System.Windows.Media.FontFamily]::new($Family)
    $typeface = [System.Windows.Media.Typeface]::new(
        $fontFamily,
        [System.Windows.FontStyles]::$Style,
        [System.Windows.FontWeights]::$Weight,
        [System.Windows.FontStretches]::Normal
    )
    $formattedText = [System.Windows.Media.FormattedText]::new(
        $Text,
        $Culture,
        [System.Windows.FlowDirection]::LeftToRight,
        $typeface,
        $Size,
        [System.Windows.Media.Brushes]::Black,
        1.0
    )
    $geometry = $formattedText.BuildGeometry([System.Windows.Point]::new(0, 0)).GetOutlinedPathGeometry()
    $bounds = $geometry.Bounds
    $d = $geometry.ToString($Culture) -replace '^F[01]', ''

    if ($TargetWidth -gt 0) {
        $ScaleX = $TargetWidth / $bounds.Width
    }

    $a = Format-Number $ScaleX
    $dScale = Format-Number $ScaleY
    $e = Format-Number ($X - ($bounds.X * $ScaleX))
    $f = Format-Number ($Y - ($bounds.Y * $ScaleY))
    $opacityAttr = if ($Opacity) { " opacity=`"$Opacity`"" } else { "" }

    return "<path d=`"$d`" fill=`"$Fill`" fill-rule=`"evenodd`" transform=`"matrix($a 0 0 $dScale $e $f)`"$opacityAttr />"
}

function New-SpacedTextPaths {
    param(
        [string]$Text,
        [string]$Family,
        [string]$Weight,
        [string]$Style,
        [double]$Size,
        [double[]]$Positions,
        [double]$Y,
        [string]$Fill
    )

    $paths = New-Object System.Collections.Generic.List[string]
    for ($i = 0; $i -lt $Text.Length; $i++) {
        $paths.Add((New-TextPath -Text $Text[$i] -Family $Family -Weight $Weight -Style $Style -Size $Size -X $Positions[$i] -Y $Y -Fill $Fill))
    }
    return ($paths -join "`n")
}

function Get-Defs {
    param([string]$Mode)

    $dropMask = @"
<mask id="drop-cutout" maskUnits="userSpaceOnUse">
  <rect x="0" y="0" width="1231" height="480" fill="white" />
  <circle cx="120" cy="241" r="43" fill="none" stroke="black" stroke-width="7" />
  <path d="M121 219 C111 236 103 247 103 257 C103 270 112 279 121 279 C130 279 139 270 139 257 C139 247 131 236 121 219 Z" fill="black" />
</mask>
"@

    return @"
<defs>
  <linearGradient id="drop-blue" x1="66" y1="120" x2="178" y2="296" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#4F8DBC" />
    <stop offset="0.58" stop-color="#126DA4" />
    <stop offset="1" stop-color="#005D93" />
  </linearGradient>
  <linearGradient id="tag-dark" x1="333" y1="351" x2="889" y2="351" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#111718" />
    <stop offset="0.35" stop-color="#20282E" />
    <stop offset="1" stop-color="#394249" />
  </linearGradient>
$dropMask
</defs>
"@
}

function Get-DropMark {
    param([string]$Mode, [string]$Ink)

    $outer = "M120 120 C103 150 84 184 73 215 C60 251 71 296 120 296 C169 296 181 251 168 215 C157 184 137 150 120 120 Z"
    $innerDrop = "M121 219 C111 236 103 247 103 257 C103 270 112 279 121 279 C130 279 139 270 139 257 C139 247 131 236 121 219 Z"

    if ($Mode -eq "white") {
        return @"
<g id="drop-mark">
  <path d="$outer" fill="$Ink" mask="url(#drop-cutout)" />
</g>
"@
    }

    $fill = if ($Mode -eq "color") { "url(#drop-blue)" } else { $Ink }
    return @"
<g id="drop-mark">
  <path d="$outer" fill="$fill" />
  <circle cx="120" cy="241" r="43" fill="none" stroke="#FFFFFF" stroke-width="7" />
  <path d="$innerDrop" fill="#FFFFFF" />
</g>
"@
}

function Get-Fendipetroleo {
    param([string]$Mode, [string]$Ink)

    $wordFill = if ($Mode -eq "white") { $Ink } else { "#050505" }
    if ($Mode -ne "color") { $wordFill = $Ink }
    $subFill = if ($Mode -eq "color") { "#2C2C2C" } else { $Ink }

    $word = New-TextPath -Text "FENDIPETROLEO" -Family "Arial" -Weight Bold -Style Normal -Size 56 -X 192 -Y 185 -TargetWidth 532 -Fill $wordFill
    $national = New-SpacedTextPaths -Text "NACIONAL" -Family "Arial" -Weight Normal -Style Normal -Size 32 -Positions @(232,296,362,433,498,562,627,694) -Y 237 -Fill $subFill

    return @"
<g id="fendipetroleo-wordmark">
  $word
  <path d="M188 227.5 H724" stroke="$subFill" stroke-width="2.4" stroke-linecap="square" />
  $national
</g>
"@
}

function Get-ComceMark {
    param([string]$Mode, [string]$Ink)

    $dark = if ($Mode -eq "color") { "#363E44" } else { $Ink }
    $green = if ($Mode -eq "color") { "#2FB344" } else { $Ink }
    $blue = if ($Mode -eq "color") { "#173D80" } else { $Ink }

    $top = New-TextPath -Text "COM" -Family "Arial Black" -Weight Black -Style Normal -Size 96 -X 873 -Y 132 -TargetWidth 248 -Fill $dark
    $bottom = New-TextPath -Text "CE" -Family "Arial Black" -Weight Black -Style Normal -Size 96 -X 870 -Y 219 -TargetWidth 160 -Fill $dark
    $oAcute = [char]0x00F3
    $desc1Text = "Confederaci" + $oAcute + "n"
    $desc5Text = "y Energ" + [char]0x00E9 + "ticos"

    $desc1 = New-TextPath -Text $desc1Text -Family "Segoe UI" -Weight Bold -Style Normal -Size 15.8 -X 1031 -Y 220 -Fill $blue
    $desc2 = New-TextPath -Text "de Distribuidores" -Family "Segoe UI" -Weight Bold -Style Normal -Size 15.8 -X 1031 -Y 236 -Fill $blue
    $desc3 = New-TextPath -Text "Minoristas de" -Family "Segoe UI" -Weight Bold -Style Normal -Size 15.8 -X 1031 -Y 252 -Fill $blue
    $desc4 = New-TextPath -Text "Combustibles" -Family "Segoe UI" -Weight Bold -Style Normal -Size 15.8 -X 1031 -Y 268 -Fill $blue
    $desc5 = New-TextPath -Text $desc5Text -Family "Segoe UI" -Weight Bold -Style Normal -Size 15.8 -X 1031 -Y 284 -Fill $blue

    return @"
<g id="comce-mark">
  $top
  $bottom
  <path d="M878 142 L866 173 L856 173 L872 190 L862 217 L893 179 L880 180 L896 145 Z" fill="$green" />
  <path d="M963 113 C985 117 1005 123 1018 137" fill="none" stroke="$green" stroke-width="6.2" stroke-linecap="round" />
  <path d="M1015 126 L1033 133 L1020 146 Z" fill="$green" />
  <path d="M1017 139 C1024 163 1014 188 992 198 C973 207 950 200 938 183" fill="none" stroke="$green" stroke-width="7" stroke-linecap="round" />
  <path d="M1003 145 C1015 152 1015 171 1002 181 C990 190 971 185 967 171 C963 158 970 145 984 141 C991 139 998 141 1003 145 Z" fill="$green" opacity="0.92" />
  <path d="M997 134 C1007 137 1015 144 1020 153" fill="none" stroke="$dark" stroke-width="5.5" stroke-linecap="round" opacity="0.9" />
  <g id="comce-descriptor">
    $desc1
    $desc2
    $desc3
    $desc4
    $desc5
  </g>
</g>
"@
}

function Get-UnityBand {
    param([string]$Mode, [string]$Ink)

    $line = if ($Mode -eq "color") { "#D9D9D9" } else { $Ink }
    $tagFill = if ($Mode -eq "color") { "url(#tag-dark)" } elseif ($Mode -eq "white") { "none" } else { $Ink }
    $tagStroke = if ($Mode -eq "white") { $Ink } else { "none" }
    $tagStrokeAttr = if ($Mode -eq "white") { " stroke=`"$tagStroke`" stroke-width=`"3`"" } else { "" }
    $tagOpacity = if ($Mode -eq "white") { " opacity=`"0.96`"" } else { "" }
    $textFill = if ($Mode -eq "mono") { "#FFFFFF" } else { "#FFFFFF" }
    if ($Mode -eq "white") { $textFill = $Ink }

    $sloganText = ([char]0x00A1) + "Somos uno!"
    $slogan = New-TextPath -Text $sloganText -Family "Arial" -Weight Bold -Style Italic -Size 58 -X 431 -Y 374 -TargetWidth 357 -Fill $textFill

    return @"
<g id="unity-band">
  <path d="M53 350 H1168" stroke="$line" stroke-width="3.6" stroke-linecap="square" opacity="0.82" />
  <path d="M333 351 H889 V409 C889 427 876 440 858 440 H364 C346 440 333 427 333 409 Z" fill="$tagFill"$tagStrokeAttr$tagOpacity />
  $slogan
</g>
"@
}

function Build-LogoSvg {
    param(
        [ValidateSet("color","mono","white")][string]$Mode,
        [bool]$Compact = $false
    )

    $ink = if ($Mode -eq "white") { "#FFFFFF" } elseif ($Mode -eq "mono") { "#30363B" } else { "#111111" }
    $viewBox = if ($Compact) { "40 95 1140 225" } else { "0 0 1231 480" }
    $width = if ($Compact) { "1140" } else { "1231" }
    $height = if ($Compact) { "225" } else { "480" }

    $defs = Get-Defs -Mode $Mode
    $drop = Get-DropMark -Mode $Mode -Ink $ink
    $fendi = Get-Fendipetroleo -Mode $Mode -Ink $ink
    $comce = Get-ComceMark -Mode $Mode -Ink $ink
    $band = if ($Compact) { "" } else { Get-UnityBand -Mode $Mode -Ink $ink }

    return @"
<svg xmlns="http://www.w3.org/2000/svg" width="$width" height="$height" viewBox="$viewBox" role="img" aria-labelledby="title desc">
<title id="title">COMCE Fendipetroleo</title>
<desc id="desc">Reconstruccion vectorial fiel del logo compuesto COMCE Fendipetroleo Nacional.</desc>
$defs
$drop
$fendi
$comce
$band
</svg>
"@
}

$outputs = @(
    @{ Name = "logoComce.svg"; Mode = "color"; Compact = $false },
    @{ Name = "logoComce-mono.svg"; Mode = "mono"; Compact = $false },
    @{ Name = "logoComce-white.svg"; Mode = "white"; Compact = $false },
    @{ Name = "logoComce-compact.svg"; Mode = "color"; Compact = $true }
)

foreach ($output in $outputs) {
    $svg = Build-LogoSvg -Mode $output.Mode -Compact ([bool]$output.Compact)
    $path = Join-Path $OutDir $output.Name
    Set-Content -LiteralPath $path -Value $svg -Encoding UTF8
    Write-Host "Wrote $path"
}
