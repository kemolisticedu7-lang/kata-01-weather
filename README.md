
Kata 8 – API Client Testing, Git Tasks, and Stretch

Overview

This kata focuses on testing an API client without making real network calls, using mocking techniques. It also demonstrates Git workflow concepts including cherry-picking commits and creating pull requests.

⸻

Tests Implemented

The API client tests were implemented using pytest and unittest.mock.

The following scenarios were tested:
    •    Successful API request – verifies that the client correctly handles a successful HTTP response.
    •    HTTP error handling – ensures the client handles non-200 responses properly.
    •    Timeout handling – confirms the client behaves correctly when a request times out.
    •    Retry logic – verifies that the client retries requests when failures occur and eventually succeeds.
    •    Observation fetching with mocks – tests the fetch_all_observations() function without calling the real FRED API.

All tests pass locally using:
pytest kata-03/tests/test_api_client.py -q

⸻

Git Task – Cherry Pick

For the Git task, I used git cherry-pick to apply a single commit containing the API client tests onto a separate branch.

Steps performed:
    1.    Identified the commit containing the completed tests.
    2.    Switched to a new branch for the demonstration.
    3.    Used git cherry-pick to apply the specific commit.
    4.    Pushed the branch to GitHub.

Example commands used:
git switch main
git switch -c kata-08-cherry-pick
git cherry-pick <commit-hash>
git push -u origin kata-08-cherry-pick

Cherry-picking differs from merging because it applies only a specific commit rather than the full branch history. This is useful when one isolated change needs to be moved to another branch.

Pull Request

A pull request was created to merge the cherry-picked changes into the main branch.
This allows the changes to be reviewed before integration.

⸻

Stretch Goal

The stretch goal suggested using libraries such as responses or httpretty for HTTP mocking.

For this implementation, unittest.mock was used to mock HTTP requests, which satisfied the kata requirement of testing the API client without performing real network calls.

 Result

All API client tests pass successfully:
5 passed
This confirms that:
	•	retry logic works correctly
	•	HTTP errors and timeouts are handled
	•	API responses are mocked properly
	•	the API client behaves as expected without external dependencies
:::
