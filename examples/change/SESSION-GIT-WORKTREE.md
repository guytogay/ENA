# Session / coding Agent safe change with Git worktree

Use this example when the Agent works in a Git repository and a new session plus durable repository state can serve as the external recovery path.

This is a reference sequence, not a universal Git policy. Adapt branch names, test commands and restart/reload steps to the real repository.

## Preconditions

Before starting:

- the repository is under Git;
- important uncommitted work has already been committed, stashed or backed up deliberately;
- the current known-good commit can be identified;
- a human or later Agent session can access the repository if the current session fails.

Do not run destructive cleanup merely to make the worktree appear clean.

## 1. Record the known-good state

From the main working tree:

```bash
git status --short
git rev-parse --show-toplevel
git rev-parse HEAD
```

Record the resulting commit as `base_commit` in the safe-change package.

If `git status --short` shows unrelated uncommitted work, preserve it deliberately before continuing.

## 2. Create an isolated change worktree

Choose a unique change ID and create a branch/worktree from the known-good commit:

```bash
git branch ena-change/CHANGE_ID BASE_COMMIT
git worktree add ../REPO-NAME-CHANGE_ID ena-change/CHANGE_ID
```

The original worktree remains on the known-good state while the Agent edits and tests the isolated worktree.

Record in `rescue.yaml`:

```yaml
profile: session
known_good:
  commit: BASE_COMMIT
change_branch: ena-change/CHANGE_ID
change_worktree: ../REPO-NAME-CHANGE_ID
recovery_actor: HUMAN_OR_NEW_SESSION
```

## 3. Make one bounded change

Inside the isolated worktree:

```bash
cd ../REPO-NAME-CHANGE_ID
# edit only the intended change
git status --short
git diff
# run the repository's relevant tests/checks
git add PATHS_FOR_THIS_CHANGE
git commit -m "Describe the bounded change"
git rev-parse HEAD
```

Record the new commit as `change_commit`.

Prefer one reviewable commit for this example. If the real change requires multiple commits, record the exact commit range and prepare a rollback appropriate to that history.

## 4. Prepare recovery before applying to the main worktree

For this one-commit example, the preferred recovery after application is normally:

```bash
git revert --no-edit CHANGE_COMMIT
```

Why `revert` rather than a blind `reset --hard`:

- it preserves later repository history;
- it expresses recovery as the inverse of the exact change;
- it is safer if another valid commit was added after the change.

If `git revert` reports a conflict, stop and let the human/new session inspect the conflict. Do not force a destructive reset over unrelated work.

Put the exact command and `BASE_COMMIT` / `CHANGE_COMMIT` in the recovery package before the live/main branch changes.

## 5. Apply only when the main worktree has not diverged

Return to the main worktree and verify its HEAD is still `BASE_COMMIT`:

```bash
git rev-parse HEAD
git status --short
```

If the branch moved or acquired unrelated changes, stop and rebuild/rebase the candidate against the new current state instead of forcing it.

If it is still safe to apply:

```bash
git merge --ff-only ena-change/CHANGE_ID
```

`--ff-only` intentionally refuses to apply when the main branch has diverged.

Set the safe-change package state to `applied`.

## 6. Verify useful operation

Run the real post-change checks, for example:

```text
repository tests/checks
Agent/tool startup if applicable
human-visible reply or new-session verification
specific task the change was meant to improve
```

A clean Git merge alone does not prove the change is useful.

If verification succeeds, set the package state to `retained`.

## 7. Recover from a bad change

A human or fresh Agent session can inspect the safe-change package and run:

```bash
git revert --no-edit CHANGE_COMMIT
```

Then rerun the required tests/startup/communication check and set the package state to `restored` when useful operation is back.

If the revert conflicts, stop and inspect. The prepared `BASE_COMMIT` is still a reference for comparison/recovery, but do not discard unrelated newer work with a forced reset unless an authorized recovery plan explicitly requires it.

## 8. Clean up only after the result is settled

After the change is either retained or restored and no longer needs the extra worktree:

```bash
git worktree remove ../REPO-NAME-CHANGE_ID
```

The change branch may be kept for history or deleted according to the repository's normal policy.

Keep the ENA safe-change package while it still carries useful recovery/history evidence.
