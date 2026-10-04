# CI release-body checks require release tags

Runs #72 (`aef012b`, v0.12.0) and #74 (`0d2ce81`, main) failed in both Python reproduction
jobs. In all four jobs the 474 numerical checks passed. The failure was the same unit test:
`ReleaseBodyStatusTests.test_a_body_whose_tag_does_not_exist_says_so`.

The workflow used the default `actions/checkout@v4` checkout. It fetches one commit, without the
historical release tags. The test reads `git tag --list`, so it classified ten historical release
bodies as untagged. A successful empty tag list did not establish that those versions were absent
from the repository; it established that the checkout lacked their refs.

## Controlled reproduction

At `0d2ce81`, a fresh `git clone --depth 1 --no-tags` contained zero tags. Running
`python -m unittest discover -s tests -p test_release_docs.py -v` failed with the same ten-body list.
In that same clone, `git fetch --unshallow --tags origin` supplied twelve release tags. Running
the identical two tests then passed, including the negative control that rejects an unmarked body
whose version genuinely has no tag. No source or release body changed between the two runs.

## Fix and scope

The `repro` job checks out with `fetch-depth: 0`, which fetches the complete history and tag set
for the release-body comparison. Both Python matrix entries use that checkout. Test logic,
experimental values, tolerances, tier selection and negative controls remain in force.

This repairs the input to the guard rather than skipping the guard or adding misleading draft
markers to historical published bodies. The old run conclusions and released tag remain historical
evidence; a new successful run must be cited for the repair.

The scorer and Docker jobs omit Git metadata in their experiment copies and already report that
the repository tag comparison is skipped there; their success did not validate this comparison.
The pure negative control still runs in those copies. Do not equate their green state with coverage
of the Git-dependent check.

Official checkout behavior: [actions/checkout documentation](https://github.com/actions/checkout#usage).
