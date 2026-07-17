# MESC Pilot-01 -- P01-03A Storage Boundary

Freeze date: 2026-07-17

## Proposed absolute path

Raw-data root:

`C:\Users\Shehr\MedScaleData\mesc-pilot-01\raw\pubmedqa`

Revision-specific directory:

`C:\Users\Shehr\MedScaleData\mesc-pilot-01\raw\pubmedqa\9001f2853fb87cab8d220904e0de81ac6973b318\pqa_labeled`

## Path-resolution evidence

Read-only inspection from canonical main worktree provided the following evidence:

* `C:\Users\Shehr\MedScaleData` does not currently exist
* proposed path does not currently exist
* no parent directory was created during this inspection
* home directory `C:\Users\Shehr` contains no `.git` repository
* OneDrive path `C:\Users\Shehr\OneDrive` exists, but the proposed path lies outside it
* no junction, symlink, or reparse point can redirect the non-existent path into a tracked or synchronized location
* Windows path resolution appears normal with no unexpected redirection detected
* filesystem permissions for later local-only research access cannot be verified without creating the directory; current evidence does not block the proposed boundary

## Creation evidence

Directory chain created in a separate authorized founder turn.

Creation timestamp:

```text
CREATION_TIMESTAMP: 2026-07-17T23:50:00Z
```

Resolved absolute path:

```text
RESOLVED_PATH: C:\Users\Shehr\MedScaleData\mesc-pilot-01\raw\pubmedqa\9001f2853fb87cab8d220904e0de81ac6973b318\pqa_labeled
```

Directory existence:

```text
DIRECTORY_EXISTS: True
```

Reparse-point status:

```text
REPARSE_POINT: False
```

Owner:

```text
OWNER: ABDULAZIZ\Shehr
```

ACL summary:

```text
NT AUTHORITY\SYSTEM:(I)(OI)(CI)(F)
BUILTIN\Administrators:(I)(OI)(CI)(F)
ABDULAZIZ\Shehr:(I)(OI)(CI)(F)
```

Inherited ACL state:

```text
INHERITED_ACL: True
```

Explicit ACL entries:

```text
EXPLICIT_ENTRIES: SYSTEM, Administrators, Shehr full control with object-inheritance and container-inheritance
```

Git/worktree exclusion:

```text
GIT_WORKTREE_EXCLUDED: True
```

OneDrive exclusion:

```text
ONEDRIVE_EXCLUDED: True
```

Temporary probe lifecycle:

```text
PROBE_FILE: .medscale-storage-probe.tmp
PROBE_CREATE: Success
PROBE_READ_METADATA: Success
PROBE_RENAME: Success
PROBE_DELETE: Success
PROBE_LEFT_BEHIND: False
```

Empty-directory confirmation:

```text
DIRECTORY_EMPTY_AFTER_PROBE: True
```

No dataset acquisition occurred:

```text
DATASET_ACQUIRED: False
```

## External-storage requirements

Acquisition, if later authorized, must write only to the proposed external path and must fail if the path would resolve inside any Git worktree, repository root, or synchronized cloud directory.

Committed authority documents require that raw abstracts must not be committed to Git and must not be published or redistributed. External storage is the controlling requirement.

## Git-worktree exclusion

All known worktrees at time of inspection:

```
C:/Users/Shehr/OneDrive/Desktop/MedScaleFiles/MedScale-align-16-audit
C:/Users/Shehr/AppData/Local/Temp/medscale-pr19-post-merge
C:/Users/Shehr/OneDrive/Desktop/MedScaleFiles/MedScale-align-16-clean
C:/Users/Shehr/OneDrive/Desktop/MedScaleFiles/MedScale-align-17-adr
C:/Users/Shehr/OneDrive/Desktop/MedScaleFiles/MedScale-align-17-closeout
C:/Users/Shehr/OneDrive/Desktop/MedScaleFiles/MedScale-mesc-p01-02-revision-lock
C:/Users/Shehr/OneDrive/Desktop/MedScaleFiles/MedScale-mesc-p01-03-closeout
C:/Users/Shehr/OneDrive/Desktop/MedScaleFiles/MedScale-mesc-p01-03-planning
C:/Users/Shehr/OneDrive/Desktop/MedScaleFiles/MedScale-pilot-01-foundation
C:/Users/Shehr/OneDrive/Desktop/MedScaleFiles/MedScale-mesc-pubmedqa-metadata-allowlist
C:/Users/Shehr/OneDrive/Desktop/MedScaleFiles/MedScale-mesc-pubmedqa-storage-boundary
```

Proposed path `C:\Users\Shehr\MedScaleData\...` is outside every listed worktree and repository root.

## Cloud-sync exclusion

Proposed path is outside `C:\Users\Shehr\OneDrive` and any other explicitly identified synchronized tree. Cloud-sync coverage cannot be guaranteed for all possible Windows configurations without explicit system policy review, but current path evidence does not indicate OneDrive coverage.

## Permissions verification

Windows filesystem permissions for `C:\Users\Shehr\MedScaleData` were verified after directory creation.

Permission probe passed:

* temporary probe file created successfully
* temporary probe file metadata readable
* temporary probe file renamed successfully
* temporary probe file deleted successfully
* directory empty after probe deletion

ACL fail-closed properties:

* ordinary inherited user/group access removed
* current user full control granted
* SYSTEM full control retained
* Administrators full control retained
* permissions inherit to child files and directories

## Retention and cleanup

Retention policy adopted in this turn. See `decision-record.md` and the committed storage-boundary documentation for the full policy.

## Directory-created confirmation

Directory chain was created during this authorized turn.

No dataset file was created.
