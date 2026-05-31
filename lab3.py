import os
import numpy as np
import matplotlib.pyplot as plt

# 1. Початкові дані (Варіант 1)
lambd = 0.025  # Довжина хвилі в метрах (2.5 см)
a_p = 0.10     # Розмір розкриву a_p в метрах (10 см)
b_p = 0.10     # Розмір розкриву b_p в метрах (10 см)

# =====================================================================
# АВТОМАТИЧНЕ СТВОРЕННЯ ПАПКИ ДЛЯ ГРАФІКІВ
# =====================================================================
folder_name = "lab3_plots"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"Папку '{folder_name}' успішно створено!")

# Задаємо масив кутів від -90 до +90 градусів з малим кроком для точної оцінки
theta_deg = np.linspace(-90.0, 90.0, 100000)
theta_rad = np.radians(theta_deg)

# --- РОЗРАХУНОК У ПЛОЩИНІ E ---
# Множник системи (без невизначеності в 0)
arg_E = (np.pi * b_p / lambd) * np.sin(theta_rad)
F_CE = np.where(theta_deg == 0, 1.0, np.sin(arg_E) / arg_E)
F_CE = np.where(np.isnan(F_CE), 1.0, F_CE)

# Множник Гюйгенса
F_1E = (1 + np.cos(theta_rad)) / 2

# Повна нормована ДС у площині E
F_E = np.abs(F_CE * F_1E)

# --- РОЗРАХУНОК У ПЛОЩИНІ H ---
# Множник системи з урахуванням граничних значень (правило Лопіталя)
arg_H = (np.pi * a_p / lambd) * np.sin(theta_rad)
denom_H = 1.0 - ((2.0 * a_p / lambd) * np.sin(theta_rad))**2

F_CH = np.zeros_like(theta_deg)
for i in range(len(theta_deg)):
    if abs(denom_H[i]) < 1e-5:
        F_CH[i] = np.pi / 4  # Граничне значення за Лопіталем
    elif theta_deg[i] == 0:
        F_CH[i] = 1.0
    else:
        F_CH[i] = np.cos(arg_H[i]) / denom_H[i]

# Множник Гюйгенса
F_1H = (1 + np.cos(theta_rad)) / 2

# Повна нормована ДС у площині H
F_H = np.abs(F_CH * F_1H)

# --- АНАЛІЗ ХАРАКТЕРИСТИК ДС ---
# Пошук ширины головної пелюстки (рівень 0.707) для позитивних кутів
pos_mask = theta_deg >= 0
theta_pos = theta_deg[pos_mask]
F_E_pos = F_E[pos_mask]
F_H_pos = F_H[pos_mask]

# Знаходження кута, найближчого до 0.707
idx_E_0707 = np.argmin(np.abs(F_E_pos - 0.707))
hpbw_E = 2 * theta_pos[idx_E_0707]

idx_H_0707 = np.argmin(np.abs(F_H_pos - 0.707))
hpbw_H = 2 * theta_pos[idx_H_0707]

print("\n=== РЕЗУЛЬТАТИ РОЗРАХУНКУ ===")
print(f"Ширина ДС у площині E (на рівні 0.707): {hpbw_E:.2f} град.")
print(f"Ширина ДС у площині H (на рівні 0.707): {hpbw_H:.2f} град.")
print("=============================\n")

# --- ПОБУДОВА ГРАФІКІВ ---
plt.figure(figsize=(10, 6))
plt.plot(theta_deg, F_E, label='Площина E (F_E)', color='blue', linewidth=2)
plt.plot(theta_deg, F_H, label='Площина H (F_H)', color='red', linestyle='--', linewidth=2)
plt.axhline(y=0.707, color='green', linestyle=':', label='Рівень 0.707 (-3 дБ)')

plt.title('Нормовані діаграми спрямованості пірамідального рупора (Варіант 1)', fontsize=12)
plt.xlabel('Кут theta, градуси', fontsize=10)
plt.ylabel('|F(theta)|', fontsize=10)
plt.xlim([-90, 90])
plt.ylim([0, 1.05])
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend(loc='upper right')

# =====================================================================
# АВТОМАТИЧНЕ ЗБЕРЕЖЕННЯ ГРАФІКА У ФАЙЛ
# =====================================================================
file_path = os.path.join(folder_name, "diagram_variant_1.png")
plt.savefig(file_path, dpi=300, bbox_inches='tight')
print(f"Графік успішно збережено за шляхом: {file_path}")

# Відображення вікна з графіком
plt.show()