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
