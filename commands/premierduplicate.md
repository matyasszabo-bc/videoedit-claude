# /premierduplicate

Duplicate the active sequence.

## Usage

```
/premierduplicate
/premierduplicate "v2 - color grade"
```

- No argument: appends ` - Copy` to the sequence name.
- With argument: uses the provided string as a suffix.

## Process

1. Get the active sequence name via BuzzRolls.
2. Duplicate the sequence.
3. Name the duplicate: `<original_name> - <suffix>`.
4. Set the duplicate as the active sequence.
5. Confirm: report the new sequence name.
