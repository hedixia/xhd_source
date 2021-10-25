from matplotlib import pyplot as plt
import numpy as np
colors = ('b', 'y', 'g', 'r', 'm', 'c', 'k')


def plot(x, y, labels, colors=colors, xlabel='x', ylabel='y', ylim=None, legend='upper left', filename=None):
    # Size check
    n = len(x)
    assert len(y) == n
    assert len(labels) == n
    assert len(colors) >= n

    # Plot
    if legend == 'outside':
        plt.figure(figsize=(17, 12))
    else:
        plt.figure(figsize=(12, 12))
    font_size = 50
    axes = plt.gca()
    axes.tick_params(axis='x', labelsize=font_size)
    axes.tick_params(axis='y', labelsize=font_size)
    for i in range(n):
        notnan = (~np.isnan(x[i])) & (~np.isnan(y[i]))
        plt.plot(x[i][notnan], y[i][notnan], linewidth=5, color=colors[i], label=labels[i])
    plt.xlabel(xlabel, fontsize=font_size)
    plt.ylabel(ylabel, fontsize=font_size)
    plt.grid(b=True, which='major', color='#666666', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
    if legend:
        if legend == 'outside':
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=font_size)
        else:
            plt.legend(loc=legend, fontsize=font_size)
    if ylim:
        plt.ylim(ylim)
    plt.tight_layout()
    if filename is not None:
        plt.savefig(filename)
    plt.show()
