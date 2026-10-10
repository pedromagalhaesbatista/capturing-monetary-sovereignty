#!/usr/bin/env python3
"""Reproduce reported descriptive results from the frozen CSVs, without network access.

No semantic coding occurs here. This checks computation and decision propagation,
not the correctness of the underlying interpretation of primary documents.
"""
from pathlib import Path
from collections import Counter
from decimal import Decimal
import csv
import json
from reconcile_reviews import reconcile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'results'
FLAGS = [
    'deposit_displacement_bank_funding', 'monetary_policy_transmission',
    'financial_stability_run_risk', 'payments_vs_investment',
    'legal_classification', 'competition_innovation_consumer_welfare',
    'commercial_viability',
]
POSITIONS = ['permit', 'permit conditionally', 'prohibit', 'ambiguous', 'no position', 'unknown']


def read_csv(relative):
    with (ROOT / relative).open(encoding='utf-8-sig', newline='') as file:
        return list(csv.DictReader(file))


def write_csv(name, rows):
    if not rows:
        return
    with (OUT / name).open('w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_json(name, data):
    (OUT / name).write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')


def private(row):
    return row['observation_kind'] == 'named_input' and row['actor_type'] != 'Public authority'


def true(value):
    return value == 'true'


def main():
    OUT.mkdir(exist_ok=True)
    actors = read_csv('data/actor_episode.csv')
    sources = read_csv('data/source_register.csv')
    scopes = read_csv('audit/observation_review_scope.csv')
    scope_by_id = {row['observation_id']: row for row in scopes}
    actor_by_id = {row['observation_id']: row for row in actors}
    source_by_id = {row['source_id']: row for row in sources}
    assert len(actor_by_id) == len(actors), 'Duplicate observation IDs'
    assert len(source_by_id) == len(sources), 'Duplicate source IDs'
    assert set(scope_by_id) == set(actor_by_id), 'Review-scope join does not cover all observations'
    for row in actors:
        assert set(json.loads(row['source_ids'])) <= set(source_by_id), row['observation_id']
        assert row['position'] in POSITIONS + [''], row['position']
        assert all(row[field] in ['yes', 'no', ''] for field in FLAGS), row['observation_id']

    named_private = [row for row in actors if private(row)]
    table = []
    for code, label in [('EU', 'European Union'), ('UK', 'United Kingdom'), ('US', 'United States'), ('ALL', 'Total')]:
        include = lambda row: code == 'ALL' or row['jurisdiction'] == code
        table.append({'jurisdiction': label, 'source_records': sum(include(row) for row in sources), 'actor_episodes': sum(include(row) for row in actors), 'named_private_actor_episodes': sum(include(row) for row in named_private)})
    assert table == [
        {'jurisdiction': 'European Union', 'source_records': 598, 'actor_episodes': 232, 'named_private_actor_episodes': 125},
        {'jurisdiction': 'United Kingdom', 'source_records': 208, 'actor_episodes': 114, 'named_private_actor_episodes': 88},
        {'jurisdiction': 'United States', 'source_records': 1370, 'actor_episodes': 171, 'named_private_actor_episodes': 137},
        {'jurisdiction': 'Total', 'source_records': 2176, 'actor_episodes': 517, 'named_private_actor_episodes': 350},
    ], 'Table 1 differs from the frozen manuscript'
    write_csv('table1.csv', table)

    def population(row):
        if row['observation_kind'] == 'named_input':
            return 'named_public_authority' if row['actor_type'] == 'Public authority' else 'named_private'
        return row['observation_kind']
    populations = Counter(population(row) for row in actors)
    assert dict(populations) == {'named_private': 350, 'named_public_authority': 22, 'anonymous_input': 81, 'institutional_policy': 58, 'anonymous_aggregate': 6}
    write_csv('populations.csv', [{'population': key, 'actor_episodes': populations[key]} for key in sorted(populations)])
    stance = Counter(row['position'] or 'unknown' for row in named_private)
    write_csv('stance_counts.csv', [{'position': position, 'actor_episodes': stance[position], 'denominator': len(named_private)} for position in POSITIONS])

    heatmap = []
    for actor_type in sorted({row['actor_type'] for row in named_private}):
        group = [row for row in named_private if row['actor_type'] == actor_type]
        heatmap.append({'actor_type': actor_type, 'n_observations': len(group), **{field: sum(row[field] == 'yes' for row in group) for field in FLAGS}, **{field + '_classifiable_n': sum(row[field] != '' for row in group) for field in FLAGS}})
    reference = read_csv('reference/original_heatmap_cells.csv')
    as_strings = [{key: str(value) for key, value in row.items()} for row in heatmap]
    assert as_strings == reference, 'Recomputed heatmap differs from the archived original cell matrix'
    assert len(heatmap) == 23 and sum(row['n_observations'] for row in heatmap) == 350
    write_csv('heatmap_cells.csv', heatmap)

    categories = []
    for category in 'ABCDE':
        counts = Counter(json.loads(row['categories']).get(category) for row in named_private)
        for position, count in sorted(counts.items(), key=lambda item: str(item[0])):
            categories.append({'category': category, 'position': position if position is not None else 'unknown', 'actor_episodes': count, 'eligible_private_actor_episodes': 350})
    write_csv('category_counts.csv', categories)

    reviewed = [row for row in scopes if true(row['second_review_record_present'])]
    complete = [row for row in reviewed if true(row['strict_complete_context_second_review'])]
    negatives = [row for row in named_private if row['position'] == 'no position']
    negative_scope = Counter('strict_complete_context' if true(scope_by_id[row['observation_id']]['strict_complete_context_second_review']) else 'qualified' if true(scope_by_id[row['observation_id']]['second_review_record_present']) else 'not_in_second_review' for row in negatives)

    reconciliation = reconcile()
    mismatches = [row for row in reconciliation if not row['matches']]
    decisions = json.loads((ROOT / 'audit/adjudication_decisions.json').read_text(encoding='utf-8'))

    claims = {
        'source_records': len(sources), 'actor_episodes': len(actors), 'named_private_actor_episodes': len(named_private),
        'private_stance': {key: stance[key] for key in POSITIONS},
        'private_substantive_or_mixed_stance': sum(stance[key] for key in ['permit', 'permit conditionally', 'prohibit', 'ambiguous']),
        'second_reviews': len(reviewed), 'strict_complete_context_second_reviews': len(complete),
        'qualified_second_reviews': len(reviewed) - len(complete), 'not_in_second_review': len(scopes) - len(reviewed),
        'no_position_second_review': dict(negative_scope),
        'field_reconciliation_comparisons': len(reconciliation), 'field_reconciliation_mismatches': len(mismatches),
        'adjudicated_observations': len(decisions),
        'figure_classifiable_denominators': [sum(row[field] != '' for row in named_private) for field in FLAGS],
    }
    expected = json.loads((ROOT / 'reference/expected_claims.json').read_text(encoding='utf-8'))
    assert claims == expected, 'Key claims do not match the independently retained reference: ' + repr(claims)
    write_json('key_claims.json', claims)

    # This sensitivity excludes heterogeneous negatives; it does not change a code.
    sensitivity = []
    keep_strict_negative = lambda row: row['position'] not in ['', 'no position'] or true(scope_by_id[row['observation_id']]['strict_complete_context_second_review'])
    for name, group in [('frozen_private_cohort', named_private), ('exclude_no_position_without_strict_second_review_keep_unknown', [row for row in named_private if row['position'] != 'no position' or true(scope_by_id[row['observation_id']]['strict_complete_context_second_review'])]), ('strict_second_review_for_negative_or_unknown', [row for row in named_private if keep_strict_negative(row)])]:
        counts = Counter(row['position'] or 'unknown' for row in group)
        sensitivity.append({'scenario': name, 'eligible_actor_episodes': len(group), **{position: counts[position] for position in POSITIONS}})
    write_csv('negative_coverage_sensitivity.csv', sensitivity)

    backlog = read_csv('audit/backlog_1011_followup.csv')
    assert len(backlog) == len({row['source_id'] for row in backlog}) == 1011
    assert set(row['source_id'] for row in backlog) <= set(source_by_id)
    distribution = Counter(row['final_administrative_status'] for row in backlog)
    assert sum(distribution.values()) == 1011
    write_csv('backlog_1011_status_counts.csv', [{'final_administrative_status': key, 'source_register_entries': distribution[key]} for key in sorted(distribution)])
    historical_statuses = Counter(row['disposition_normalized'] for row in sources)
    write_csv('historical_source_dispositions.csv', [{'historical_disposition': key, 'source_register_entries': historical_statuses[key]} for key in sorted(historical_statuses)])

    # Rounded scenario arithmetic only, not replication of either economic model.
    external = read_csv('data/comparative_scenarios.csv')
    no_interest, with_interest = external
    deposit_gap = Decimal(with_interest['deposit_decline_percent']) - Decimal(no_interest['deposit_decline_percent'])
    capacity_gap = Decimal(with_interest['reduction_in_lending_capacity_USD_billions']) - Decimal(no_interest['reduction_in_lending_capacity_USD_billions'])
    assert deposit_gap == Decimal('19.7') and capacity_gap == Decimal('1250')
    write_json('comparative_scenario_arithmetic.json', {'source': no_interest['source_url'], 'deposit_decline_difference_percentage_points': str(deposit_gap), 'lending_capacity_reduction_difference_USD_billions': str(capacity_gap), 'qualification': 'Subtraction of rounded reported scenarios, not a causal estimate, independent model replication or harmonisation with the CEA model.'})

    evidence = read_csv('evidence/passage_ledger.csv')
    assert all(row['observation_id'] in actor_by_id and row['source_id'] in source_by_id for row in evidence)
    write_json('validation.json', {'status': 'passed', 'scope': 'Computational reproduction and recorded-decision propagation only; no independent semantic recoding or live-URL availability check.', 'source_ids_unique': True, 'actor_episode_ids_unique': True, 'all_actor_source_ids_present': True, 'all_passage_source_ids_present': True, 'original_heatmap_cells_match': True, 'table1_matches': True, 'key_claims_match': True, 'network_required': False})
    print('PASS: Table 1, 161 heatmap cells, stance/coverage claims, 4,800 decision-field comparisons and scenario arithmetic.')
    print('Results: ' + str(OUT))


if __name__ == '__main__':
    main()
