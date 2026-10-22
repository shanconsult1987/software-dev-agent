$inputText = [Console]::In.ReadToEnd()

$blockedPatterns = @(
    "git push --force",
    "git reset --hard",
    "Remove-Item -Recurse",
    "rm -rf"
)

foreach ($pattern in $blockedPatterns) {

    if (
        $inputText -match
        [regex]::Escape($pattern)
    ) {

        Write-Error "BLOCKED: $pattern"

        exit 1
    }
}

Write-Output "VALIDATION PASSED"

exit 0
