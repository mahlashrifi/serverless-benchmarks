import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


if __name__ == "__main__":
    platforms = ["aws", "azure", "gcp"]
    name = sys.argv[-1] if len(sys.argv) > 1 else "parallel"

    funcs = ["gen_buffer_one", "gen_buffer_two", "gen_buffer_three", "gen_buffer_four", "gen_buffer_five"]
    invos = list(zip(funcs, funcs[1:]))

    fig, ax = plt.subplots()

    for platform in platforms:
        path = os.path.join("cache", "results", name, platform+".csv")
        if not os.path.exists(path):
            continue

        df = pd.read_csv(path)

        ys = []
        for a, b in invos:
            end = df.loc[(df["func"] == a)]["end"].to_numpy()
            start = df.loc[(df["func"] == b)]["start"].to_numpy()
            ys.append(start-end)

        ys = np.asarray(ys)
        ys = np.mean(ys, axis=0)
        xs = np.arange(ys.shape[0])

        line = ax.plot(xs, ys)[0]
        line.set_label(platform)

    ax.set_title("function invocation")
    ax.set_xlabel("repetition")
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.set_xticks(np.arange(0, len(xs)+1, 5))
    ax.set_ylabel("latency [s]")
    fig.legend()

    plt.show()