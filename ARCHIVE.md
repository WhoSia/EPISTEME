# EPISTEME — Full-History Custody and Retirement Record

**Current official generation:** [EPISTEME-P77 — Research Identity Adjudication: Historical Testability, Philosophical Reconstitution & Terminal Review](https://app.notion.com/p/40eef561cf9281bd9b7be9700af4ab53) (confirmed 2026-11-04). The P77 naming update does not modify the historical source tree or the SHA-sealed pre-compaction archive.

## Full verified pre-compaction archive

- Source repository: `WhoSia/EPISTEME`, default branch `main`.
- Archived commit: `5404b640ce24e4788ac9b7c300b88a676294aa57` (Git tree `fd0471ed842e14de6a3a2f44c71b495c2d0c52ac`).
- 415 tracked files (pre-compaction).
- GitHub Actions read-only custody workflow `.github/workflows/p77_custody_snapshot.yml`.
- **Run:** [#41759741803](https://github.com/WhoSia/EPISTEME/actions/runs/41759741803) — `SUCCESS`.
- **Artifact ID:** `13289518140`; source artifact SHA-256: `df7aa87ab0067b76e735b258e0b6a2b00bf203dc6aec0d89dbb5fa790d18080c`.
- **Drive byte-custody copy:** [`EPISTEME_P77_FULL_HISTORY_5404b640_20261104.zip`](https://drive.google.com/file/d/1tC16je1yu9JHSP7jajiNXITJAfM5n_k_/view), file ID `1tC16je1yu9JHSP7jajiNXITJAfM5n_k_`.
- **Archive SHA-256:** `df7aa87ab0067b76e735b258e0b6a2b00bf203dc6aec0d89dbb5fa790d18080c`. Verified against the downloaded Drive copy, not just the upload response.
- ZIP contains `episteme-full-history.bundle` (all history, HEAD/ref), `episteme-head.tar.gz` (full snapshot of tracked source at the frozen head), `tracked_paths.txt` (complete 415-file index), `git_tree.txt`, `HEAD.txt`, `HEAD_commit.txt`, `SHA256SUMS.txt` and `GOVERNANCE.txt`.
- `sha256sum -c SHA256SUMS.txt` passed on all five recorded payloads; independent `git clone episteme-full-history.bundle` restored the same frozen HEAD and all 415 tracked files. No bot Git author or writeback.

## Compaction policy

The original README was a 56 kB chronological accumulation whose headline still described P76 as latest active. It is replaced by a short **current-status entrypoint**, not by rewriting source history.

Retire older `active/p16–p76` stage receipts not listed in current README, discontinued P69–P76 runner implementations, unused CI workflow programs, seven historical manuscripts, abandoned EPISTEME 2.0 candidate and ancillary historic source fixtures from the live tree. **All source bytes and original Git lineage survive in the verified Drive archive and pinned Git commit.** Current P77 courts, critical negative results, NeXus source-pair tests and governing policies remain live.

Retirement is **administrative archiving, not evidence that every past file is false or scientifically irrelevant**. Every historical hypothesis, failed test, experimental input and old manuscript retains original timestamps and Git identities within the bundle.

### Retrieval / restoration

1. Download the Drive ZIP, verify its external SHA-256 above, unzip.
2. From the extracted folder, run `sha256sum -c SHA256SUMS.txt`.
3. To inspect original source: `tar -xzf episteme-head.tar.gz`.
4. To restore the exact pre-retirement repository history: `git clone episteme-full-history.bundle EPISTEME-full-history`, then verify `git -C EPISTEME-full-history rev-parse HEAD` is `5404b640...`.
5. To cite a previous path without restoring: use `https://github.com/WhoSia/EPISTEME/blob/5404b640ce24e4788ac9b7c300b88a676294aa57/<original-path>`.
6. Do not treat the old branch's historical `OPEN` labels as current EPISTEME research authority. [RESEARCH_STATUS.md](RESEARCH_STATUS.md) controls present status.

**Deletion and closure are separate.** The GitHub repository and verified archive remain accessible; retiring old branches/files does not authorize deleting the repository.
