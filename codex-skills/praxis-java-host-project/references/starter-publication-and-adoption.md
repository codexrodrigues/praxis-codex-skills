# Starter publication and public host adoption

The starter repository owns its publication pipeline; the host consumes the
published artifact. Inspect exact source/tag/version, `pom.xml`, release workflow,
`RELEASING.md` and available operational tools before recommending a command.
Do not infer public availability from a local install, tag, passing tests or upload.

For Config's reviewed bundle-gate candidate, inspect
`tools/release/central_bundle.py`, `publish_central.py` and their offline tests.
Confirm that these files exist in the actual immutable release revision before
using this route. Metadata has a different wrapper/lifecycle and requires its own
review; a shared publisher version does not prove identical behavior or defects.

Preserve mandatory source/version/JUnit/signature gates. The candidate runs signed
`clean verify`, selects the real flattened POM, main/sources/javadoc JARs and four
ASC signatures, and builds only the expected versioned Maven directory. Its separate
archive validator requires unique safe paths, exact entry set, checksums, POM and
main JAR Maven identity, and a valid detached signature from the expected signer.
Never manufacture a POM at artifactId root, include repository metadata, weaken
Central validation or fix a renamed historical JAR by adjusting receipt hashes.

The same archive bytes and SHA-256 must be validated, preserved as a sanitized
artifact, then uploaded once through the official Publisher API. Bind the receipt
to the actual source commit/tree and version tag. Keep credentials only in the
upload step, never argv/logs/artifact settings or GPG keys. Refuse authenticated
redirects. Preserve the returned deployment UUID immediately, before status polling.
Bound publication and each HTTP call to the remaining official job budget,
reserving explicit time for final custody artifacts. Refuse a new upload when
that margin is exhausted; do not increase the job limit by reflex.
On uncertain upload, failed status, rejected validation or wait exhaustion, keep
original evidence and reconcile the same attempt; never automatically reupload,
move a tag or delete a failed deployment. A workflow rerun is not a new upload
permission. Consult Config's existing `central-deployment-status.yml` when an ID
exists. Plugin 0.10/0.11 `skipPublishing` is not a demonstrated safe bundle-only
lane: inspect implementation, not just a configuration option's description.

Offline packaging/transport tests may use an explicitly identified signature
verifier fixture and injected transport. They prove selection/control logic,
not OpenPGP verification or live publication. Actual GPG signing and verification
remain mandatory before an official upload; do not introduce a production bypass
or install an alternative crypto mechanism to make a local test appear complete.
Record source freeze, runtime, argv, actual exit, log hash and exclusive TMP cleanup.
Preserve original failed and earlier limited runs rather than replacing receipts.

`PUBLISHED` must identify the expected coordinate. Then resolve actual public
POM/JAR bytes and checksums, update the host's pinned dependency, and validate
without a local public-coordinate install or version override. Attest the resolved
artifact and packaged nested JAR, then prove the affected protected HTTP path.
Publication does not certify operational migrations, hosted role provisioning,
deployment, Angular or whole-backend readiness. Keep those gates explicit and
reuse valid source-bound tests without reflexively repeating complete suites.

For Metadata's separately reviewed bundle-gate candidate, retain its Maven 3.9.6
wrapper, full signed `clean verify`, public contract hygiene gate and documentation
job dependency. Its 90-minute job budget is measured from the first step; upload,
status and public availability share the remaining deadline and custody reserve.
Do not copy Config's 45-minute value or add independent propagation windows.
Verify the actual public POM and main JAR plus their SHA-512 checksums against the
validated archive, without installing that public coordinate locally. Wrong bytes
or exhausted availability retain the deployment and prevent adoption. Inspect
these helpers in the immutable source before relying on this candidate path;
offline fixtures still do not certify the official signature or publication.

A socket timeout does not bound the whole open/read operation. The Metadata
candidate also guards the complete call with a POSIX timer in its own Python main
thread, restores the signal handler, refuses an existing timer and rejects a late
return before certifying availability. Verify blocking-operation and final-read
deadline tests; do not claim these controls from fixtures that only mock a clock.
When changing a release route, inventory existing Java and Python workflow
contract tests before release. Update obsolete publisher literals to assert the
retained signed test gates, ordering, custody and unique upload; do not delete
those tests or weaken the release gates to obtain a green job.

The separately reviewed Config total-operation deadline candidate uses the same
own-Python POSIX guard, while retaining Config's45-minute job/180-second custody
reserve and its own GAV. Inspect the actual immutable source and corresponding
Java/Python convention proofs before relying on it; Metadata's90-minute budget
and public availability checks must not be copied as Config guarantees.
