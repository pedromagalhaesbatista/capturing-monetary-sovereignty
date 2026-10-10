CAPTURING MONETARY SOVEREIGNTY — REPLICATION PACKAGE
Version v1.0.0 | 10 October 2026 | substantive source cutoff 2 October 2026
Author: Pedro M Batista

START HERE
This is the small, shareable computational companion to the paper. It contains
the recorded data, definitions, source links, coding audit and executable code.
Repository: https://github.com/pedromagalhaesbatista/capturing-monetary-sovereignty
The author's original data and documentation are licensed under CC BY 4.0; original
code is licensed under MIT. Third-party excerpts and metadata are excluded from
these grants. Read LICENSE.txt and RIGHTS.txt for the precise scope.

You do not need to program to inspect the results. Open results/table1.csv,
results/stance_counts.csv, results/heatmap_cells.csv and results/key_claims.json.
The PDF/PNG/SVG figure is supplied in results/ and can be regenerated.
Two unchanged PDFs are retained in reference/: the research_v2 archive figure
and manuscript_figure1.pdf, the artwork used for the manuscript. The regenerated
plot follows the research_v2 design; the manuscript styling may differ.
reference/figure_versions.json identifies their hashes and roles. A CSV is a table that Excel,
Numbers or a text editor can open. JSON stores structured records; a text editor
can read it. Avoid saving over the frozen input CSVs when opening them in Excel.

WHAT THIS PACKAGE REPRODUCES
Table 1: 2,176 source-register entries; 517 actor–episodes; 350 named private inputs.
Figure 1: the original 23 actor-type by 7 rationale cell counts and fieldwise denominators.
Holder-stance totals: 12 permit, 10 conditional, 27 prohibit, 34 ambiguous, 245 no recorded
position, 22 unknown; 83 have a recorded substantive/mixed stance. It also regenerates
review counts, negative-coverage sensitivity and the 1,011-entry supplementary audit.

Reproduction means obtaining the same counts from the same recorded classifications.
It is not independent replication of the source interpretation. Source links,
pinpoints and scope statements allow a reviewer to examine that interpretation.
No API, model call, network retrieval or original research folder is required to
calculate the results. Third-party texts are linked, not bundled as a raw corpus.

HOW TO RUN
1. Install Python 3.12 or later for the full package (tested with Python 3.12.14).
   The numerical scripts alone also support Python 3.10 or later. The pinned
   plotting dependencies require Python 3.12 or later. Open a terminal in this folder.
2. Before regenerating files, check the delivered package’s hashes:
      python3 scripts/verify_manifest.py
3. Reproduce the numerical results and decision reconciliation:
      python3 scripts/reproduce.py
   This uses only Python’s standard library and requires no package installation.
   It writes deterministic CSV/JSON results and checks them against frozen reference
   cells/claims. A failure stops with an explanation rather than silently changing data.
4. To draw Figure 1 as PDF, PNG and SVG, create and activate a virtual environment:
      python3 -m venv .venv
      source .venv/bin/activate
   Then install the plotting dependencies and draw the figure:
      python3 -m pip install -r requirements.txt
      python3 scripts/plot_heatmap.py
   On Windows activate with .venv\Scripts\activate and use python instead of python3.
   Installation may require internet access. Once dependencies are installed,
   computation and plotting operate offline.

The manifest verifies the files as delivered. Rerendering with different fonts,
operating systems or library versions can change figure bytes while the numeric
cell checks still pass. A later figure-hash difference is therefore not by itself
an analytical discrepancy; input-data and numeric-output changes need explanation.
requirements-lock.txt records the full tested plotting dependency set.

DATA AND AUDIT MAP
data/actor_episode.csv — 517 final analytic rows; all counts start here.
data/source_register.csv — 2,176 provenance/availability entries, not 2,176 unique texts.
evidence/actor_source_links.csv — explicit joins from actor episodes to sources.
evidence/passage_ledger.csv — active evidence, with source IDs, URLs and pinpoints.
evidence/passage_roles.csv — why passage rows must not be counted as votes.
evidence/v04_v05_public_source_map.json — dated historical and decisive actor
checks, with source URLs, hashes, pinpoints and final-code links.
evidence/final_review_v01_v03_source_checks.json — later legal and model-scenario
source checks. data/comparative_scenarios.csv reproduces only subtraction of
Nigrinis’s rounded scenarios, not the underlying economic model.
methods/final_codebook.txt — final category and missingness definitions.
methods/data_dictionary.csv — field guide for the retained input columns.
methods/instrument_reconciliation.txt — what changed and what can be verified.
audit/field_reconciliation.csv — the archived 4,800 field comparisons.
audit/second_review_codes.json — the recorded second-session codes, used with
adjudication_decisions.json by scripts/reconcile_reviews.py to reconstruct final
values afresh whenever reproduce.py runs.
audit/observation_review_scope.csv — scope for all 517 rows; includes 197 without a
second review and coverage warnings. No second review is not no first reading.
audit/no_position_unknown_coverage.csv — all 245 no-position and 22 unknown private rows.
audit/backlog_1011_followup.csv — one final administrative status per audited entry.
audit/historical_argument_rows.csv — prior/inactive evidence retained for audit only.
supplements/ — later qualitative checks. These do not alter the frozen figure/counts.
reference/ — original figure cells and input hashes, used as independent checks.

HOW TO CHECK ONE CLAIM
Find the actor in data/actor_episode.csv and note its observation_id. Read its
categories, position, source_ids and coverage fields. Follow the same ID in
evidence/actor_source_links.csv and evidence/passage_ledger.csv. Open the primary
source URL and read the cited page with its surrounding contribution. Use the
final actor-category code for quantitative counts. A V2ADJ passage can explain a
mixed overall decision; its category/position cross-product is not a separate vote.
For a no-position record, inspect coverage before treating it as an absence claim.

BOUNDARIES
One actor in several proceedings contributes several actor–episodes. A joint
coalition is one observation. Anonymous inputs, official policy documents and
named public-authority inputs are not part of Figure 1’s 350 private observations.
Rationales are nonexclusive; a row may contribute to several columns. The figure
counts stated rationales across A–E, including issuer-income positions; it does
not estimate stakeholder preferences or establish causal regulatory capture.
Zeros are not opposition. Blank analytic fields mean unknown, not zero.

The 1,011-entry audit distinguishes direct readings, targeted readings, index pages,
links and unresolved leads. Linked coverage is not inherited. It is not a count
of 1,011 missing unique documents. Source-register status and source-wide semantic
coverage are different concepts. Read audit/backlog_status_definitions.json.

PROVENANCE AND VERSIONING
The quantitative snapshot is the existing research_v2_2026-10-02 dataset, whose
eligibility cutoff is 2 October. Coding refinements/reviews followed that cutoff;
version v1.0.0 was prepared 10 October 2026. The 9 October supplement is qualitative.
reference/source_snapshots.json records original input hashes and package hashes.
Original archive-relative locations are provenance labels only; the raw archive is
not required or distributed here. Author-local absolute paths have been removed.
Local reviewer checks and manifests establish file identity, not semantic accuracy.

CITATION AND REUSE
Cite Pedro M Batista, Capturing Monetary Sovereignty: Replication Package,
v1.0.0 (10 October 2026), using CITATION.cff.
Version v1.0.0 archive DOI: https://doi.org/10.5281/zenodo.23272352
Record the version used and describe any changes to the data or code. The data
remain the frozen research snapshot described above; a release number does not
imply new source coding.
