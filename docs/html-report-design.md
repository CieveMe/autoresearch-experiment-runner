# Offline per-run HTML export

The existing HTML-export TODO is implemented as a separate, standard-library
command that reads an existing `results.json` and writes one self-contained
HTML file. Unlike adding an automatic output to every runner invocation, this
keeps the accepted numerical pipeline and its artifacts unchanged. Unlike a
JavaScript dashboard, it requires no installation or network connection.

The report contains experiment identity, configuration and source hashes,
the original hypothesis, all trial metrics and training curves as inline SVG.
Table order uses the runner's metric direction and tie-breaker. It describes
the recorded best arm as a single-run ranking, without interpreting ties as
statistical significance or asserting expected-value verification. Threshold
not configured and threshold not reached have distinct labels. Input text is
escaped; there are no executable scripts or external assets. The command must
refuse to overwrite its input. The seed and full trial configuration remain
available in expandable details.

Acceptance: deterministic output for the same source; source bytes unchanged;
lower/higher metric direction, ties, null thresholds, absent curves, unequal
curve lengths and HTML injection handled; CLI round trip succeeds on real
committed artifacts. Unit suite must remain green. No new experimental axes,
training, release, DOI or paper changes are part of this feature.
