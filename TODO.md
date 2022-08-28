- Specify the format of the judge output
    - the output has to be in valid json format
    - if not, judge error will be raised
```json=
{
    "status": "judging/judged",
    "score": 123,
    "subtasks": [
        ["subtask 1", "JE", 0, 10],
        ["subtask 2", "AC", 10, 10],
        ["subtask 3", "RE", 0, 10],
        ["subtask 4", "WA", 0, 10]
    ]
}
```

- Use python-docker
- Show problems according to the viewer's uid (only the Admin can see hidden problems)
- A system to save / reload the problems
- An ID check has to happen somewhere when uploading a new problem
- Add problem visibility
- a page to check the result
- Use abort instead of returns to check logins