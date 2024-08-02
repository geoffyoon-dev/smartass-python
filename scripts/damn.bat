@set PYTHONIOENCODING=utf-8
@powershell -noprofile -c "cmd /c \"$(smartass %* $(doskey /history)[-2])\"; [Console]::ResetColor();"
