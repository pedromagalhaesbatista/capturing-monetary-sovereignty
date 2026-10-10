#!/usr/bin/env python3
"""Regenerate the original figure design from verified exact cell counts.

PDF/PNG bytes can vary across font/rendering/library versions; numeric cells and
labels are checked by reproduce.py. No primary-source interpretation occurs here.
"""
from pathlib import Path
import csv
import sys
import os

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / '.matplotlib'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from reproduce import main, FLAGS
main()
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

with (ROOT / 'results/heatmap_cells.csv').open(encoding='utf-8') as file:
    rows = list(csv.DictReader(file))
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10, 'svg.fonttype': 'none', 'svg.hashsalt': 'stablecoin-v2-20261002', 'pdf.fonttype': 42, 'savefig.facecolor': 'white'})
labels = ['Deposit /\nbank funding', 'Monetary\ntransmission', 'Stability /\nrun risk', 'Payments /\ninvestment', 'Legal\nclassification', 'Competition /\nconsumer\nwelfare', 'Commercial\nviability']
data = np.array([[int(row[field]) for field in FLAGS] for row in rows])
fig, ax = plt.subplots(figsize=(14, max(7, len(rows) * .33 + 2.4)))
im = ax.imshow(data, cmap='Blues', vmin=0, vmax=max(1, data.max()), aspect='auto')
ax.set_yticks(range(len(rows)), [row['actor_type'] + ' (n=' + row['n_observations'] + ')' for row in rows])
ax.set_xticks(range(7), labels)
ax.xaxis.tick_top()
ax.tick_params(length=0, pad=10, labelsize=9)
for i in range(len(rows)):
    for column in range(7):
        ax.text(column, i, str(data[i, column]), ha='center', va='center', fontsize=9, color='white' if data[i, column] > data.max() * .56 else '#243542')
for spine in ax.spines.values():
    spine.set_visible(False)
ax.set_title('Stated rationales across A–E in named private actor–episodes', loc='left', pad=55, fontsize=17, fontweight='bold')
fig.colorbar(im, ax=ax, shrink=.5, label='Actor–episode count', pad=.02)
fig.text(.02, .025, 'Labels include no-position, E-only and unknown records; fieldwise classifiable denominators are in the CSV.\nRationales are nonexclusive and count once per actor–episode. Repeat actors across episodes remain separate.\nPublic authorities and anonymous inputs are excluded. These availability-selected counts do not estimate stakeholder preferences.', fontsize=9, color='#52616e')
fig.subplots_adjust(left=.30, right=.95, top=.81, bottom=.12)
metadata = {'Creator': 'Bounded comparative stablecoin remuneration study v2', 'CreationDate': None, 'ModDate': None}
for extension in ['png', 'svg', 'pdf']:
    fig.savefig(ROOT / ('results/actor_type_rationale_heatmap.' + extension), dpi=240, metadata=metadata if extension == 'pdf' else {'Date': None} if extension == 'svg' else {'Software': 'Stablecoin research v2'})
plt.close(fig)
print('Figure written as PDF, PNG and SVG in results/.')
