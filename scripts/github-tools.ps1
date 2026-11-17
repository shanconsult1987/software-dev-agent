
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("issue", "prs", "runs", "repo")]
    [string]$Action,

    [string]$IssueNumber
)

$ErrorActionPreference = "Stop"

gh auth status

switch ($Action) {

    "issue" {
        if (-not $IssueNumber) {
            throw "IssueNumber is required"
        }

        gh issue view $IssueNumber
    }

    "prs" {
        gh pr list
    }

    "runs" {
        gh run list
    }

    "repo" {
        gh repo view
    }
}
