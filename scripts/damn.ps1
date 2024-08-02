if ((Get-Command "damn").CommandType -eq "Function") {
	damn @args;
	[Console]::ResetColor()
	exit
}

"First time use of smartass detected. "

if ((Get-Content $PROFILE -Raw -ErrorAction Ignore) -like "*smartass*") {
} else {
	"  - Adding smartass intialization to user `$PROFILE"
	$script = "`n`$env:PYTHONIOENCODING='utf-8' `niex `"`$(smartass --alias)`"";
	Write-Output $script | Add-Content $PROFILE
}

"  - Adding damn() function to current session..."
$env:PYTHONIOENCODING='utf-8'
iex "$($(smartass --alias).Replace("function damn", "function global:damn"))"

"  - Invoking damn()`n"
damn @args;
[Console]::ResetColor()
