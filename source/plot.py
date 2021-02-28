import matplotlib.pyplot as plt


def plot_solution(positions, sol, color):
    plt.title("Optimized tour")
    plt.scatter(positions[:, 0], positions[:, 1], color=color)  # plot B
    n = len(sol)
    for i in range(n - 1):
        node_i = positions[sol[i]]
        node_j = positions[sol[i + 1]]
        plt.annotate(
            "",
            xy=node_i,
            xycoords="data",
            xytext=node_j,
            textcoords="data",
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
            color=color,
        )
    plt.annotate(
        "",
        xy=node_j,
        xycoords="data",
        xytext=positions[sol[0]],
        textcoords="data",
        arrowprops=dict(arrowstyle="->", connectionstyle="arc3"),
        color=color,
    )
    plt.tight_layout()
    return plt
