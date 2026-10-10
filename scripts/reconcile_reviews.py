#!/usr/bin/env python3
"""Reconstruct final reviewed codes from retained second codes + adjudications."""
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['position', 'unspecified_holder_position', 'reserve_safety_distribution_distinguished', 'deposit_displacement_bank_funding', 'monetary_policy_transmission', 'financial_stability_run_risk', 'payments_vs_investment', 'legal_classification', 'competition_innovation_consumer_welfare', 'commercial_viability'] + ['category_' + c for c in 'ABCDE']


def get_code(row, field, csv_row=False):
    if field.startswith('category_'):
        categories = json.loads(row['categories']) if csv_row else row['categories']
        return categories.get(field[-1], 'not_addressed')
    if field == 'unspecified_holder_position':
        return row.get(field) or 'not_addressed'
    return (row.get(field) or None) if csv_row else row.get(field)


def reconcile():
    with (ROOT / 'data/actor_episode.csv').open(encoding='utf-8-sig', newline='') as file:
        final = {row['observation_id']: row for row in csv.DictReader(file)}
    second = json.loads((ROOT / 'audit/second_review_codes.json').read_text(encoding='utf-8'))
    decisions = json.loads((ROOT / 'audit/adjudication_decisions.json').read_text(encoding='utf-8'))
    adjudications = {row['observation_id']: row for row in decisions}
    assert len(adjudications) == len(decisions), 'Duplicate adjudication observation IDs'
    assert len(second) == len({row['observation_id'] for row in second}) == 320
    assert set(adjudications) <= {row['observation_id'] for row in second}
    comparisons = []
    for row in sorted(second, key=lambda item: item['observation_id']):
        oid = row['observation_id']
        overrides = adjudications.get(oid, {}).get('final_values', {})
        for field in FIELDS:
            second_code = get_code(row, field)
            reconstructed = overrides[field] if field in overrides else second_code
            recorded = get_code(final[oid], field, csv_row=True)
            comparisons.append({'observation_id': oid, 'field': field, 'second_code': second_code, 'adjudication_override_present': field in overrides, 'reconstructed_final_code': reconstructed, 'recorded_final_code': recorded, 'matches': reconstructed == recorded})
    mismatches = [row for row in comparisons if not row['matches']]
    assert not mismatches, 'Reconstructed decisions differ from final actor codes: ' + repr(mismatches[:10])
    assert len(comparisons) == 4800
    output = ROOT / 'results'
    output.mkdir(exist_ok=True)
    with (output / 'review_propagation.csv').open('w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=list(comparisons[0]))
        writer.writeheader()
        writer.writerows(comparisons)
    return comparisons


if __name__ == '__main__':
    comparisons = reconcile()
    print('PASS: reconstructed ' + str(len(comparisons)) + ' reviewed fields from second codes and adjudication decisions.')
