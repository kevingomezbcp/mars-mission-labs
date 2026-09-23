import os
import matplotlib.pyplot as plt

os.makedirs("generated_formulas", exist_ok=True)

def render_latex(formula_str, output_filename, fontsize=18, textcolor="#222222", bg_color=None, dpi=300):
    fig = plt.figure(figsize=(0.1, 0.1), dpi=dpi)
    if bg_color:
        fig.patch.set_facecolor(bg_color)
    else:
        fig.patch.set_alpha(0.0)
        
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    if bg_color:
        ax.set_facecolor(bg_color)
    else:
        ax.patch.set_alpha(0.0)
        
    t = ax.text(0.5, 0.5, formula_str, fontsize=fontsize, color=textcolor,
                ha='center', va='center', usetex=False)
    
    # Save figure
    filepath = os.path.join("generated_formulas", output_filename)
    fig.savefig(filepath, bbox_inches='tight', pad_inches=0.1, transparent=(bg_color is None), dpi=dpi)
    plt.close(fig)
    print(f"Rendered: {filepath}")
    return filepath

# Test formulas
f1 = render_latex(r"$P(y \mid x) = \prod_{t=1}^{T} P(y_t \mid y_{<t}, x; \theta)$", "formula_classical.png", fontsize=20, textcolor="#333333")
f2 = render_latex(r"$P(y \mid x) = \sum_{d \in \mathcal{D}} P(d \mid x) \cdot P(y \mid x, d; \theta)$", "formula_rag_bayes.png", fontsize=22, textcolor="#C3338E")
f3 = render_latex(r"$\mathrm{RRF\_Score}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$", "formula_rrf.png", fontsize=20, textcolor="#C3338E")
