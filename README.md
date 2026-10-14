# logfire-google-warning

Repo with minimal example to illustrate bug.

```
(.venv) C:\Shared\Projects\Personal\logfire-google-warning>set "GEMINI_API_KEY=XXXX"

(.venv) C:\Shared\Projects\Personal\logfire-google-warning>python reproduce_warning.py
--- Calling client.models.generate_content(...) ---
14:23:06.739 generate_content gemini-3.5-flash-lite
Warning: there are non-text parts in the response: ['function_call'], returning concatenated text result from text parts. Check the full candidates.content.parts accessor to get the full model response.
--- generate_content returned successfully ---
(Notice: user code has not accessed response or response.text at all)
```