#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 29 20:47:53 2025

@author: rdx
"""

from matplotlib import pyplot as plt
from matplotlib_venn import venn3

# --- Setup figure ---
plt.figure(figsize=(12, 12))

# --- Draw Venn Diagram ---
v = venn3(
    subsets=(1, 1, 1, 1, 1, 1, 1),
    set_labels=("Ontology", "Epistemology", "Axiology")
)

# --- Base colors for each axis ---
v.get_patch_by_id('100').set_color('#ff6666')   # Ontology area
v.get_patch_by_id('010').set_color('#66cc66')   # Epistemology area
v.get_patch_by_id('001').set_color('#6699ff')   # Axiology area

# transparency
for area in ['100','010','001','110','101','011','111']:
    if v.get_patch_by_id(area):
        v.get_patch_by_id(area).set_alpha(0.45)

# --- Remove default subset labels (numbers) ---
for label in ['100','010','001','110','101','011','111']:
    if v.get_label_by_id(label):
        v.get_label_by_id(label).set_text("")

# ---------------------------------------------
# Place philosophical schools manually
# ---------------------------------------------

# Ontology only (100)
plt.text(v.get_label_by_id('100').get_position()[0] - 0.10,
         v.get_label_by_id('100').get_position()[1],
         "Eksistensialisme\nMaterialisme\nIdealism\nMetafisika Klasik",
         ha='center', fontsize=11)

# Epistemology only (010)
plt.text(v.get_label_by_id('010').get_position()[0] + 0.10,
         v.get_label_by_id('010').get_position()[1],
         "Rasionalisme\nEmpirisme\nPositivisme\nSkeptisisme",
         ha='center', fontsize=11)

# Axiology only (001)
plt.text(v.get_label_by_id('001').get_position()[0],
         v.get_label_by_id('001').get_position()[1] - 0.10,
         "Utilitarianisme\nDeontologi (hak-kewajiban)\nHedonisme",
         ha='center', fontsize=11)

# Ontology + Epistemology (110)
plt.text(v.get_label_by_id('110').get_position()[0],
         v.get_label_by_id('110').get_position()[1] + 0.05,
         "Fenomenologi\nRealisme [Kritis]",
         ha='center', fontsize=11)

# Ontology + Axiology (101)
plt.text(v.get_label_by_id('101').get_position()[0] - 0.03,
         v.get_label_by_id('101').get_position()[1] - 0.03,
         "Humanisme\nStoisisme",
         ha='center', fontsize=11)

# Epistemology + Axiology (011)
plt.text(v.get_label_by_id('011').get_position()[0] + 0.03,
         v.get_label_by_id('011').get_position()[1] - 0.03,
         "Pragmatisme\nEtika",
         ha='center', fontsize=11)

# All three (111)
plt.text(v.get_label_by_id('111').get_position()[0],
         v.get_label_by_id('111').get_position()[1],
         "Filsafat Islam-Abrahamistik (cenderung ke aksiologi)\nBuddhisme (cenderung ke epistemologi)\nVedanta (cenderung ke ontologi)",
         ha='center', fontsize=11)

# plt.title("Venn Diagram: Ontology – Epistemology – Axiology\n(Philosophical Schools)", fontsize=16)
plt.show()
