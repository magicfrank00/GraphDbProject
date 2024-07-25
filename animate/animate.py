import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import csv


def animate():
    metrics = []

    with open("metrics/metrics.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            metrics.append(row)

    neo = []
    pg = []
    for log in metrics:
        if log["manager"] == "neo":
            neo.append(log["penalty"])
        elif log["manager"] == "pg":
            pg.append(log["penalty"])
        else:
            continue

    # prefix sum
    neo = np.cumsum([float(x) for x in neo])
    pg = np.cumsum([float(x) for x in pg])

    min_len = min(len(neo), len(pg))
    neo = neo[:min_len]
    pg = pg[:min_len]

    def animate_two_series(y_data1, y_data2, save_path="animation.gif"):
        if len(y_data1) != len(y_data2):
            raise ValueError("Both input arrays must have the same length")

        fig, ax = plt.subplots()

        x_data = np.arange(len(y_data1))
        ax.set_xlim(0, len(x_data) - 1)
        ax.set_ylim(min(min(y_data1), min(y_data2)), max(max(y_data1), max(y_data2)))
        ax.set_xlabel("Action Count")
        ax.set_ylabel("Total Delay")

        (line1,) = ax.plot([], [], lw=2, label="Neo4j")
        (line2,) = ax.plot([], [], lw=2, label="Postgres")

        xdata, ydata1_list, ydata2_list = [], [], []

        def init():
            line1.set_data([], [])
            line2.set_data([], [])
            return line1, line2

        def update(frame):
            xdata.append(frame)
            ydata1_list.append(y_data1[frame])
            ydata2_list.append(y_data2[frame])

            line1.set_data(xdata, ydata1_list)
            line2.set_data(xdata, ydata2_list)
            return line1, line2

        ani = animation.FuncAnimation(
            fig, update, frames=len(x_data), init_func=init, blit=True
        )

        ax.legend()

        ani.save(save_path, writer="pillow")

        print(f"Animation saved to {save_path}")

    name = f"animation{random.randint(1,10000)}"
    animate_two_series(neo, pg, save_path=f"animations/{name}.gif")
    print(f"Animation saved to animations/{name}.gif")
    return f"animations/{name}.gif\n"


from flask import Flask

app = Flask(__name__)


@app.route("/graph", methods=["GET"])
def create_graph():
    return animate()


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
