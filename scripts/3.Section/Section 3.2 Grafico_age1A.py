import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Dados de idade
age_labels = ["Under 18", "18–24", "25–34", "35–44", "45–54", "55–64", "65+"]
age_values = [0.0, 2.6, 32.1, 46.2, 14.1, 5.1, 0.0]

# Criação do gráfico
fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(age_labels, age_values, color="steelblue", edgecolor="lightgray")

# Título e rótulos
ax.set_title("Age distribution of participants", fontsize=13)
ax.set_ylabel("% Participants", fontsize=11)
ax.set_ylim(0, 50)
ax.set_xticklabels(age_labels, rotation=0)  # Eixo X sem inclinação

# Formatador de porcentagem no eixo Y
ax.yaxis.set_major_formatter(mtick.PercentFormatter())

# Linhas de grade
ax.yaxis.grid(True, linestyle='--', linewidth=0.6, color='lightgray')
ax.set_axisbelow(True)

# Adiciona os rótulos nas barras
for bar in bars:
    height = bar.get_height()
    ax.annotate(f'{height}%', xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=9)

plt.tight_layout()
# Salvar imagem
# plt.savefig("figure1a_age_updated.png", dpi=300)
plt.show()
