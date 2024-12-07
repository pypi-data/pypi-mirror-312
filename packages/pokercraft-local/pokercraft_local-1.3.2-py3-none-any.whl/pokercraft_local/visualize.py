import math
import typing
import warnings

import numpy as np
import pandas as pd  # type: ignore [import-untyped]
import plotly.express as px  # type: ignore [import-untyped]
import plotly.graph_objects as plgo  # type: ignore [import-untyped]
from plotly.subplots import make_subplots  # type: ignore [import-untyped]

from .bankroll import analyze_bankroll
from .constants import BASE_HTML_FRAME, DEFAULT_WINDOW_SIZES
from .data_structures import TournamentBrand, TournamentSummary


def log2_or_nan(x: float | typing.Any) -> float:
    return math.log2(x) if x > 0 else math.nan


def get_historical_charts(
    tournaments: list[TournamentSummary],
    max_data_points: int = 2000,
    window_sizes: tuple[int, ...] = DEFAULT_WINDOW_SIZES,
):
    """
    Get historical charts.
    """
    df_base = pd.DataFrame(
        {
            "Tournament Name": [t.name for t in tournaments],
            "Time": [t.start_time for t in tournaments],
            "Profit": [t.profit for t in tournaments],
            "Rake": [t.rake * t.my_entries for t in tournaments],
            "Profitable": [1 if t.profit > 0 else 0 for t in tournaments],
            "Buy In": [t.buy_in for t in tournaments],
        }
    )
    df_base["Net Profit"] = df_base["Profit"].cumsum()
    df_base["Net Rake"] = df_base["Rake"].cumsum()
    df_base["Ideal Profit w.o. Rake"] = df_base["Net Profit"] + df_base["Net Rake"]
    df_base.index += 1

    # Profitable ratio
    profitable_expanding = df_base["Profitable"].expanding()
    df_base["Profitable Ratio"] = (
        profitable_expanding.sum() / profitable_expanding.count()
    )
    for window_size in window_sizes:
        this_title = f"Profitable Ratio W{window_size}"
        df_base[this_title] = (
            df_base["Profitable"].rolling(window_size).sum() / window_size
        )

    # Avg buy-in
    buyin_expanding = df_base["Buy In"].expanding()
    df_base["Avg Buy In"] = buyin_expanding.sum() / buyin_expanding.count()
    max_rolling_buyin: float = 0
    min_rolling_buyin: float = 1e9
    for window_size in window_sizes:
        this_title = f"Avg Buy In W{window_size}"
        df_base[this_title] = df_base["Buy In"].rolling(window_size).mean()
        max_rolling_buyin = max(max_rolling_buyin, df_base[this_title].max())
        min_rolling_buyin = min(min_rolling_buyin, df_base[this_title].min())

    # Resampling
    df_base = df_base.iloc[:: max(1, math.ceil(len(df_base) / max_data_points)), :]

    figure = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        row_titles=["Net Profit & Rake", "Profitable Ratio", "Average Buy In"],
        x_title="Tournament Count",
        vertical_spacing=0.01,
    )
    common_options = {
        "x": df_base.index,
        "mode": "lines",
        "customdata": np.stack((df_base["Tournament Name"],), axis=-1),
    }

    for col in ("Net Profit", "Net Rake", "Ideal Profit w.o. Rake"):
        figure.add_trace(
            plgo.Scatter(
                y=df_base[col],
                legendgroup="Profit",
                legendgrouptitle_text="Profits & Rakes",
                name=col,
                hovertemplate="%{y:$,.2f}",
                **common_options,
            ),
            row=1,
            col=1,
        )

    for window_size in (0,) + window_sizes:
        pr_col = (
            "Profitable Ratio"
            if window_size == 0
            else f"Profitable Ratio W{window_size}"
        )
        name = "Since 0" if window_size == 0 else f"Recent {window_size}"

        figure.add_trace(
            plgo.Scatter(
                y=df_base[pr_col],
                meta=[y * 100 for y in df_base[pr_col]],
                legendgroup="Profitable Ratio",
                legendgrouptitle_text="Profitable Ratio",
                name=name,
                hovertemplate="%{meta:.3f}%",
                **common_options,
            ),
            row=2,
            col=1,
        )
        avb_col = "Avg Buy In" if window_size == 0 else f"Avg Buy In W{window_size}"
        figure.add_trace(
            plgo.Scatter(
                y=df_base[avb_col],
                legendgroup="Avg Buy In",
                legendgrouptitle_text="Avg Buy In",
                name=name,
                hovertemplate="%{y:$,.2f}",
                **common_options,
            ),
            row=3,
            col=1,
        )

    figure.update_layout(
        title="Historical Performance",
        hovermode="x unified",
        yaxis1={"tickformat": "$"},
        yaxis2={"tickformat": ".2%"},
        yaxis3={"tickformat": "$"},
    )
    figure.update_traces(xaxis="x")
    figure.update_yaxes(
        row=3,
        col=1,
        patch={
            "type": "log",
            "range": [
                math.log10(max(min_rolling_buyin, 0.1)) - 0.1,
                math.log10(max(max_rolling_buyin, 0.1)) + 0.1,
            ],
        },
    )

    opacity_red = "rgba(255,0,0,0.25)"
    opacity_black = "rgba(0,0,0,0.25)"
    figure.add_hline(
        y=0.0,
        line_color=opacity_red,
        line_dash="dash",
        row=1,
        col=1,
        label={
            "text": "Break-even",
            "textposition": "end",
            "font": {"color": opacity_red, "weight": 5, "size": 24},
            "yanchor": "top",
        },
        exclude_empty_subplots=False,
    )
    for threshold, text in [
        (5.0, "Micro / Low"),
        (20.0, "Low / Mid"),
        (100.0, "Mid / High"),
    ]:
        figure.add_hline(
            y=threshold,
            line_color=opacity_black,
            line_dash="dash",
            row=3,
            col=1,
            label={
                "text": text,
                "textposition": "start",
                "font": {"color": opacity_black, "weight": 5, "size": 18},
                "yanchor": "top",
            },
            exclude_empty_subplots=False,
        )
    figure.update_shapes(xref="x domain", xsizemode="scaled", x0=0, x1=1)
    return figure


def get_profit_scatter_charts(tournaments: list[TournamentSummary]):
    """
    Get profit scatter charts.
    """
    df_base = pd.DataFrame(
        {
            "Tournament Name": [t.name for t in tournaments],
            "Buy In": [t.buy_in for t in tournaments],
            "Relative Prize": [t.relative_return + 1 for t in tournaments],
            "Prize Ratio": [t.my_prize / t.total_prize_pool for t in tournaments],
            "Total Entries": [t.total_players for t in tournaments],
            "Tournament Brand": [
                TournamentBrand.find(t.name).name for t in tournaments
            ],
            "Profitable": [t.profit > 0 for t in tournaments],
        }
    )

    figure1 = make_subplots(
        1,
        2,
        shared_yaxes=True,
        column_titles=[
            "By Buy In amount (Nonzero profit only)",
            "By Total Entries (Nonzero profit only)",
        ],
        y_title="Relative Prize Return",
        horizontal_spacing=0.01,
    )
    fig1_common_options = {
        "y": df_base["Relative Prize"].apply(log2_or_nan),
        "z": df_base["Relative Prize"],
        "customdata": np.stack((df_base["Tournament Name"],), axis=-1),
        "coloraxis": "coloraxis",
        "histfunc": "sum",
    }
    figure1.add_trace(
        plgo.Histogram2d(
            x=df_base["Buy In"].apply(log2_or_nan),
            name="RR by Buy In",
            hovertemplate="Log2(RR) = [%{y}]<br>Log2(BuyIn) = [%{x}]<br>"
            "Got %{z:.2f}x profit in this region",
            **fig1_common_options,
        ),
        row=1,
        col=1,
    )
    figure1.add_trace(
        plgo.Histogram2d(
            x=df_base["Total Entries"].apply(log2_or_nan),
            name="RR by Entries",
            hovertemplate="Log2(RR) = [%{y}]<br>"
            "Log2(TotalEntries) = [%{x}]<br>"
            "Got %{z:.2f}x profit in this region",
            **fig1_common_options,
        ),
        row=1,
        col=2,
    )
    figure1.update_layout(title="Relative Prize Returns")
    figure1.update_coloraxes(
        colorscale=[
            [0, "rgba(62, 51, 212, 0.25)"],  # blue
            [0.03, "rgba(135, 232, 26, 0.5)"],  # green
            [0.1, "rgba(232, 137, 26, 0.75)"],  # orange
            [0.3, "rgba(217, 17, 41, 0.75)"],  # red
            [1, "rgba(230, 36, 228, 0.75)"],  # purple
        ],
    )

    for y, color, hline_label in [
        (0.0, "white", "Break-even: 1x Profit"),
        (2.0, "rgb(102, 102, 102)", "Good run: 4x Profit"),
        (5.0, "rgb(46, 46, 46)", "Deep run: 32x Profit"),
    ]:
        figure1.add_hline(
            y=y,
            line_color=color,
            line_dash="dash",
            row=1,
            col="all",
            label={
                "text": hline_label,
                "textposition": "start",
                "font": {"color": color, "weight": 5, "size": 20},
                "yanchor": "top",
            },
        )

    df_base["Dot Size Multiplier"] = df_base["Relative Prize"].apply(
        lambda x: max(1 / 3.0, x ** (1 / 3.0))
    )
    figure2 = px.scatter(
        df_base,
        x="Total Entries",
        y="Buy In",
        size="Dot Size Multiplier",
        hover_data=["Relative Prize", "Prize Ratio"],
        color="Profitable",
        log_x=True,
        log_y=True,
        title="ITM Scatters",
        size_max=45,
    )

    return [figure1, figure2]


def get_bankroll_charts(
    tournaments: list[TournamentSummary],
    initial_capitals: typing.Iterable[int] = (10, 20, 50, 100, 200, 500),
):
    """
    Get bankroll charts.
    """
    try:
        analyzed = analyze_bankroll(
            tournaments,
            initial_capital_and_exits=tuple((ic, 0.0) for ic in initial_capitals),
            max_iteration=max(10000, len(tournaments) * 10),
        )
    except ValueError as err:
        warnings.warn(
            (
                "Bankroll analysis failed with reason(%s)."
                " Perhaps your relative returns are losing."
            )
            % (err,)
        )
        df_base = pd.DataFrame(
            {
                "Initial Capital": ["%.1f Buy-ins" % (ic,) for ic in initial_capitals],
                "Bankruptcy Rate": [1.0 for _ in initial_capitals],
                "Profitable Rate": [0.0 for _ in initial_capitals],
            }
        )
    else:
        df_base = pd.DataFrame(
            {
                "Initial Capital": ["%.1f Buy-ins" % (k,) for k in analyzed.keys()],
                "Bankruptcy Rate": [v.get_bankruptcy_rate() for v in analyzed.values()],
                "Profitable Rate": [v.get_profitable_rate() for v in analyzed.values()],
            }
        )

    figure = px.bar(
        df_base,
        x="Initial Capital",
        y=["Bankruptcy Rate", "Profitable Rate"],
        title="Bankroll Analysis with Monte-Carlo Simulation",
        color_discrete_sequence=["rgb(242, 111, 111)", "rgb(113, 222, 139)"],
        text_auto=True,
    )
    figure.update_yaxes(tickformat=".2%", minallowed=0.0, maxallowed=1.0)
    return figure


def plot_total(
    nickname: str,
    tournaments: typing.Iterable[TournamentSummary],
    sort_key: typing.Callable[[TournamentSummary], typing.Any] = (
        lambda t: t.sorting_key()
    ),
    max_data_points: int = 2000,
    window_sizes: tuple[int, ...] = DEFAULT_WINDOW_SIZES,
) -> str:
    """
    Plots the total prize pool of tournaments.
    """
    tournaments = sorted(tournaments, key=sort_key)
    figures = [
        get_historical_charts(
            tournaments,
            max_data_points=max_data_points,
            window_sizes=window_sizes,
        ),
        *get_profit_scatter_charts(tournaments),
        get_bankroll_charts(tournaments),
    ]
    return BASE_HTML_FRAME % (
        nickname,
        "\n".join(
            fig.to_html(include_plotlyjs=("cdn" if i == 0 else False), full_html=False)
            for i, fig in enumerate(figures)
        ),
    )
