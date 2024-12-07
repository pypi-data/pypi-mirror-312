def plot_discrete_distribution(drv, start=None, stop=None, x_max=None, highlight_color_index=0, colors=sns.palettes.color_palette('Set2'), **kwargs):
    """Plot a discrete distribution.

    Additional kwargs are passed to `sns.barplot`.

    Args:
        drv
        start
        stop
        x_max
        highlight_color_index
        colors

    Returns:
            Matplotlib Axis.

    """

    b = x_max if x_max is not None else drv.b

    x = np.arange(b + 1)
    y = [drv.pmf(i) for i in x]
    
    ax = sns.barplot(x=x, y=y, color=colors[-1], **kwargs)
    bars = ax.patches

    highlight_color = colors[highlight_color_index]

    # What if support doesn't start at zero?
    # if start is not None:
    #     start += drv.a

    if start is not None and stop is None:
        bars[start].set_facecolor(highlight_color)
        highlighted_probability = drv.pmf(start)
    elif stop is not None:
        highlight_slice = slice(start, stop+1)
        for b in bars[highlight_slice]:
            b.set_facecolor(highlight_color)    
        highlighted_probability = sum(drv.pmf(range(start, stop+1)))
    else:
        highlighted_probability = 0
    
    ax.set_title(f"Highlighted Probability: {highlighted_probability:.3f}")

    return ax

def plot_continuous_distribution(crv, x_min, x_max, cdf_x=None, n_samples=1000, **kwargs):
    """Plot a continuous distribution.
    
    Additional kwargs are passed to `sns.barplot`.

    Args:
        crv
        x_min
        x_max
        cdf_x
        n_samples

    Returns:
        Matplotlib Axis.

    """
    x = np.linspace(x_min, x_max, n_samples)
    y = crv.pdf(x)

    ax = sns.lineplot(x=x, y=y, **kwargs)

    if cdf_x is not None:
        cdf_y = crv.cdf(cdf_x)
        ax.fill_between(x, y, where=(x <= cdf_x), alpha=0.5)
    else:
        cdf_y = 0
        
    title = f'Probability of shaded region: {cdf_y:.3f}'
    ax.set_title(title)

    return ax
