# MESC Pilot-01 -- P01-03A Storage Boundary

Freeze date: 2026-07-17

## Proposed absolute path

Raw-data root:

`C:\Users\Shehr\MedScaleData\mesc-pilot-01\raw\pubmedqa\`

Revision-specific directory:

`C:\Users\Shehr\MedScaleData\mesc-pilot-01\raw\pubmedqa\9001f2853fb87cab8d220904e0de81ac6973b318\pqa_labeled\`

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
```

Proposed path `C:\Users\Shehr\MedScaleData\...` is outside every listed worktree and repository root.

## Cloud-sync exclusion

Proposed path is outside `C:\Users\Shehr\OneDrive` and any other explicitly identified synchronized tree. Cloud-sync coverage cannot be guaranteed for all possible Windows configurations without explicit system policy review, but current path evidence does not indicate OneDrive coverage.

## Permissions expectations

Directory creation was not performed. Windows filesystem permissions for `C:\Users\Shehr\MedScaleData` are unverified. Later authorization should confirm that the owner-only access boundary can be maintained.

## Retention and cleanup

Retention and cleanup policy is not yet determined. Future governance should answer:

* whether acquired artifacts are retained indefinitely or for a bounded research period
* whether deletion must produce secure erasure
* who owns cleanup after project archiving

## Directory-created confirmation

No directory was created during this readiness turn.
