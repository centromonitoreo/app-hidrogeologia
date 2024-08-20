import pandas as pd
import matplotlib.pylab as plt
import numpy as np
import math
import matplotlib.pyplot as plt
import imageio
import seaborn as sns
from tkinter import messagebox
from matplotlib.font_manager import FontProperties


def mifflin_graphic(df: pd.DataFrame, col_style: str = None, col_color: str = None):
    """
    Generate a Mifflin diagram for groundwater evolution based on the provided data.

    This function creates a scatter plot that visualizes the relationship between the concentrations
    of sodium plus potassium (Na + K) and chloride plus sulfate (Cl + SO4) in milliequivalents per liter (meq/L).
    The plot is logarithmic on both axes and includes annotations to indicate different flow regimes (Local,
    Intermediate, Regional) and groundwater evolution.

    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame containing the necessary columns for sodium (Na), potassium (K), chlorides (Cl), and
        sulfates (SO4) in milliequivalents per liter (meq/L).
    col_style : str, optional
        The name of the column to be used for styling the points in the scatter plot.
    col_color : str, optional
        The name of the column to be used for coloring the points in the scatter plot.

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The generated Mifflin diagram as a Matplotlib Figure object.

    Notes:
    ------
    - The function adds diagonal lines to indicate different flow regimes (Local, Intermediate, Regional).
    - Text annotations are added to the plot to label these regimes and the general direction of groundwater evolution.
    - The function adjusts the font size of the legend based on the number of labels and the maximum label length.
    """
    df["Na + K (meq/L)"] = df["Sodio (meq/L)"] + df["Potasio (meq/L)"]
    df["Cl + SO4 (meq/L)"] = df["Cloruros (meq/L)"] + df["Sulfatos (meq/L)"]
    df["Cl + SO4 (meq/L)"] = df["Cl + SO4 (meq/L)"].apply(abs)
    fig, ax = plt.subplots(figsize=(7.2, 5))
    sns.scatterplot(
        data=df,
        x="Cl + SO4 (meq/L)",
        y="Na + K (meq/L)",
        ax=ax,
        style=col_style,
        hue=col_color,
    )

    ax.set_xlabel("Cl + SO4 (meq/L)")
    ax.set_ylabel("Na + K (meq/L)")
    ax.set_ylim(0.1, 100)
    ax.set_yscale("log")
    ax.set_xlim(0.1, 100)
    ax.set_xscale("log")
    plt.grid()
    ax.plot([100, 0.1], [0.1, 100], "b", alpha=0.75, linewidth=0.7)
    ax.plot([100, 1], [1, 100], "b", alpha=0.75, linewidth=0.7)
    ax.text(0.2, 8, "Local Flow", {"color": "k", "fontsize": 7, "fontweight": "bold"})
    ax.text(
        0.45,
        20,
        "Intermediate Flow",
        {"color": "k", "fontsize": 7, "fontweight": "bold"},
    )
    ax.text(
        20, 35, "Regional Flow", {"color": "k", "fontsize": 7, "fontweight": "bold"}
    )
    text = "Groundwater Evolution"
    ax.text(4.5, 0.6, text, {"color": "k", "fontsize": 6}, rotation=45)
    x_start = 5
    y_start = 0.5
    x_end = 33.5
    y_end = 3.35
    ax.annotate(
        "",
        xy=(x_end, y_end),
        xytext=(x_start, y_start),
        arrowprops=dict(arrowstyle="simple", color="grey"),
    )
    plt.title("MIFFLIN Diagram")
    plt.subplots_adjust(right=0.75)
    if ax.get_legend():
        num_labels = len(ax.get_legend().get_texts())
        max_text_length = max(
            [len(text.get_text()) for text in ax.get_legend().get_texts()]
        )
        font_size_for_max_text = 150 / max_text_length
        font_size = 200 / num_labels  # Adjust this value according to your preferences
        font_size = min([font_size_for_max_text, font_size])
        font_props = FontProperties(size=font_size)
        ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", prop=font_props)
    else:
        print("No legend found in the graphic.")
    fig.tight_layout()
    return fig


def gibbs_graphic(df: pd.DataFrame, col_style: str = None, col_color: str = None):
    """
    Generate a Gibbs diagram to visualize the geochemical processes in groundwater.

    This function creates two scatter plots that represent the relationship between
    sodium/(sodium + calcium) and chloride/(chloride + bicarbonate) versus total dissolved salts
    (TDS) in milligrams per liter (mg/L). The Gibbs diagram helps to identify the dominant
    geochemical processes (e.g., evaporation, rock dominance, precipitation) affecting
    groundwater composition.

    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame containing the following columns with concentrations in milligrams per liter (mg/L):
        - 'Sodio (mg/L)'
        - 'Calcio (mg/L)'
        - 'Cloruros (mg/L)'
        - 'Bicarbonato (mg/L)'
        - 'Total dissolved salts (mg/L)'
    col_style : str, optional
        The name of the column to be used for styling the points in the scatter plots.
    col_color : str, optional
        The name of the column to be used for coloring the points in the scatter plots.

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The generated Gibbs diagram as a Matplotlib Figure object, containing two subplots
        representing the geochemical relationships.

    Notes:
    ------
    - The function includes diagonal lines to demarcate different geochemical processes, such as seawater influence,
      rock dominance, and precipitation dominance.
    - Text annotations are added to label these processes and to guide the interpretation of the plot.
    - The function adjusts the font size of the legend based on the number of labels and the maximum label length.
    """
    df["Na/(Na + Ca)"] = df["Sodio (mg/L)"] / (
        df["Sodio (mg/L)"] + df["Calcio (mg/L)"]
    )
    df["Cl/(Cl + HCO3)"] = df["Cloruros (mg/L)"] / (
        df["Cloruros (mg/L)"] + df["Bicarbonato (mg/L)"]
    )
    df["Total dissolved salts (mg/L)"] = (
        df["Sodio (mg/L)"]
        + df["Calcio (mg/L)"]
        + df["Cloruros (mg/L)"]
        + df["Bicarbonato (mg/L)"]
    )
    fig, ax = plt.subplots(1, 2, figsize=(20, 7), sharey=True)
    plt.subplots_adjust(wspace=0.1)
    sns.scatterplot(
        data=df,
        x="Na/(Na + Ca)",
        y="Total dissolved salts (mg/L)",
        ax=ax[0],
        style=col_style,
        hue=col_color,
    )
    ax[0].set_xlabel("Na/(Na + Ca)")
    ax[0].set_ylabel("Total dissolved salts (mg/L)")
    ax[0].set_ylim(1, 10000)
    ax[0].set_yscale("log")
    ax[0].set_xlim(0.0, 1)
    ax[0].grid(axis="y")
    dashed_color = "gray"
    thickness = 1
    style = "--"
    ax[0].plot([0, 0.7], [300, 10000], dashed_color, linewidth=thickness, ls=style)
    ax[0].plot([0, 1.0], [100, 1.2], dashed_color, linewidth=thickness, ls=style)
    ax[0].plot([0.55, 1.0], [250, 9000], dashed_color, linewidth=thickness, ls=style)
    ax[0].plot([0.55, 0.55], [150, 250], dashed_color, linewidth=thickness, ls=style)
    ax[0].plot([0.55, 1.0], [150, 7], dashed_color, linewidth=thickness, ls=style)
    ax[0].text(
        0.7, 6300, "Seawater", {"color": "k", "fontsize": 7, "fontweight": "bold"}
    )
    ax[0].text(
        0.05, 110, "Rock Dominance", {"color": "k", "fontsize": 7, "fontweight": "bold"}
    )
    ax[0].text(
        0.7,
        6,
        "Precipitation\nDominance",
        {"color": "k", "fontsize": 7, "fontweight": "bold"},
    )
    text = "Evaporation\nPrecipitation"
    ax[0].text(0.46, 680, text, {"color": "k", "fontsize": 8}, rotation=46)
    ax[0].annotate(
        "",
        xytext=(0.3, 200),
        xy=(0.48, 680),
        arrowprops=dict(arrowstyle="<-", color="grey"),
    )
    ax[0].annotate(
        "",
        xytext=(0.65, 2500),
        xy=(0.78, 6500),
        arrowprops=dict(arrowstyle="->", color="grey"),
    )
    text = "Series"
    ax[0].text(0.48, 18, text, {"color": "k", "fontsize": 8}, rotation=320)
    ax[0].annotate(
        "",
        xytext=(0.49, 32),
        xy=(0.3, 90),
        arrowprops=dict(arrowstyle="->", color="grey"),
    )
    ax[0].annotate(
        "",
        xytext=(0.71, 10),
        xy=(0.62, 18),
        arrowprops=dict(arrowstyle="<-", color="grey"),
    )
    sns.scatterplot(
        data=df,
        x="Cl/(Cl + HCO3)",
        y="Total dissolved salts (mg/L)",
        ax=ax[1],
        style=col_style,
        hue=col_color,
    )
    ax[1].set_xlabel("Cl/(Cl + HCO3)")
    ax[1].set_ylim(1, 10000)
    ax[1].set_yscale("log")
    ax[1].set_xlim(0.0, 1)
    ax[1].grid(axis="y")
    ax[1].plot([0, 0.7], [300, 10000], dashed_color, linewidth=thickness, ls=style)
    ax[1].plot([0, 1.0], [100, 1.2], dashed_color, linewidth=thickness, ls=style)
    ax[1].plot([0.55, 1.0], [250, 9000], dashed_color, linewidth=thickness, ls=style)
    ax[1].plot([0.55, 0.55], [150, 250], dashed_color, linewidth=thickness, ls=style)
    ax[1].plot([0.55, 1.0], [150, 7], dashed_color, linewidth=thickness, ls=style)
    ax[1].text(
        0.7, 6000, "Seawater", {"color": "k", "fontsize": 7, "fontweight": "bold"}
    )
    ax[1].text(
        0.05, 110, "Rock Dominance", {"color": "k", "fontsize": 7, "fontweight": "bold"}
    )

    fig.suptitle("GIBBS Diagram Season")
    if ax[0].get_legend():
        num_labels = len(ax[0].get_legend().get_texts())
        max_text_length = max(
            [len(text.get_text()) for text in ax[0].get_legend().get_texts()]
        )
        font_size_for_max_text = 280 / max_text_length
        font_size = 280 / num_labels  # Adjust this value according to your preferences
        font_size = min([font_size_for_max_text, font_size])
        font_props = FontProperties(size=font_size)
        ax[0].legend(bbox_to_anchor=(1.05, 1), loc="upper left", prop=font_props)
    else:
        print("No legend found in the graphic.")
    if ax[1].get_legend():
        num_labels = len(ax[1].get_legend().get_texts())
        max_text_length = max(
            [len(text.get_text()) for text in ax[1].get_legend().get_texts()]
        )
        font_size_for_max_text = 280 / max_text_length
        font_size = 280 / num_labels  # Adjust this value according to your preferences
        font_size = min([font_size_for_max_text, font_size])
        font_props = FontProperties(size=font_size)
        ax[1].legend(bbox_to_anchor=(1.05, 1), loc="upper left", prop=font_props)
    else:
        print("No legend found in the graphic.")

    fig.tight_layout()
    return fig


def piper_graphic(df: pd.DataFrame, col_style: str = None, col_color: str = None):
    """
    Generate a Piper diagram to classify the hydrochemical facies of groundwater.

    This function creates a Piper diagram by plotting the normalized concentrations of major cations
    (calcium, magnesium, sodium + potassium) and anions (chloride, sulfate, bicarbonate + carbonate) in a
    trilinear plot. The diagram is used to classify groundwater types and identify hydrochemical facies.

    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame containing the necessary columns for:
        - 'Sulfatos (meq/L)'
        - 'Bicarbonato (meq/L)'
        - 'Carbonato (meq/L)'
        - 'Cloruros (meq/L)'
        - 'Magnesio (meq/L)'
        - 'Calcio (meq/L)'
        - 'Potasio (meq/L)'
        - 'Sodio (meq/L)'
    col_style : str, optional
        The name of the column to be used for styling the points in the Piper diagram.
    col_color : str, optional
        The name of the column to be used for coloring the points in the Piper diagram.

    Returns:
    --------
    fig : matplotlib.figure.Figure
        The generated Piper diagram as a Matplotlib Figure object.

    Notes:
    ------
    - The function calculates normalized concentrations for cations and anions, which are then used to plot the
      respective points in the trilinear diagram.
    - The Piper diagram combines these trilinear plots to provide a comprehensive view of the hydrochemical
      characteristics of groundwater.
    - The function adjusts the font size of the legend based on the number of labels and the maximum label length.
    """
    img = imageio.imread("./data/PiperCompleto.png")
    df["total_anion"] = (
        df["Sulfatos (meq/L)"]
        + df["Bicarbonato (meq/L)"]
        + df["Carbonato (meq/L)"]
        + df["Cloruros (meq/L)"]
    )
    df["total_cation"] = (
        df["Magnesio (meq/L)"]
        + df["Calcio (meq/L)"]
        + df["Potasio (meq/L)"]
        + df["Sodio (meq/L)"]
    )
    df["SO4_norm"] = df["Sulfatos (meq/L)"] / df["total_anion"] * 100
    df["HCO3_CO3_norm"] = (
        (df["Bicarbonato (meq/L)"] + df["Carbonato (meq/L)"]) / df["total_anion"] * 100
    )
    df["Cl_norm"] = df["Cloruros (meq/L)"] / df["total_anion"] * 100
    df["Mg_norm"] = df["Magnesio (meq/L)"] / df["total_cation"] * 100
    df["Na_K_norm"] = (
        (df["Potasio (meq/L)"] + df["Sodio (meq/L)"]) / df["total_cation"] * 100
    )
    df["Ca_norm"] = df["Calcio (meq/L)"] / df["total_cation"] * 100
    df["xcation"] = 40 + 360 - (df["Ca_norm"] + df["Mg_norm"] / 2) * 3.6
    df["ycation"] = 40 + (math.sqrt(3) * df["Mg_norm"] / 2) * 3.6
    df["xanion"] = 40 + 360 + 100 + (df["Cl_norm"] + df["SO4_norm"] / 2) * 3.6
    df["yanion"] = 40 + (df["SO4_norm"] * math.sqrt(3) / 2) * 3.6
    df["xdiam"] = 0.5 * (
        df["xcation"] + df["xanion"] + (df["yanion"] - df["ycation"]) / math.sqrt(3)
    )
    df["ydiam"] = 0.5 * (
        df["yanion"] + df["ycation"] + math.sqrt(3) * (df["xanion"] - df["xcation"])
    )
    col_style = [] if col_style is None else [col_style]
    col_color = [] if col_color is None else [col_color]
    df_cation = df[["xcation", "ycation"] + col_style + col_color].rename(
        columns={"xcation": "x", "ycation": "y"}
    )
    df_anion = df[["xanion", "yanion"] + col_style + col_color].rename(
        columns={"xanion": "x", "yanion": "y"}
    )
    df_diam = df[["xdiam", "ydiam"] + col_style + col_color].rename(
        columns={"xdiam": "x", "ydiam": "y"}
    )
    df_fig = pd.concat([df_cation, df_anion, df_diam], ignore_index=True)
    fig, ax = plt.subplots()
    plt.imshow(np.flipud(img), zorder=0)
    col_style = None if len(col_style) == 0 else col_style[0]
    col_color = None if len(col_color) == 0 else col_color[0]
    sns.scatterplot(data=df_fig, x="x", y="y", ax=ax, style=col_style, hue=col_color)
    fig.subplots_adjust(right=0.7)
    plt.ylim(0, 830)
    plt.xlim(0, 900)
    plt.axis("off")
    if ax.get_legend():
        num_labels = len(ax.get_legend().get_texts())
        max_text_length = max(
            [len(text.get_text()) for text in ax.get_legend().get_texts()]
        )
        font_size_for_max_text = 150 / max_text_length
        font_size = 200 / num_labels  # Adjust this value according to your preferences
        font_size = min([font_size_for_max_text, font_size])
        font_props = FontProperties(size=font_size)
        ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left", prop=font_props)
    else:
        print("No legend found in the graphic.")

    fig.tight_layout()
    return fig


def stiff_graphic(df: pd.DataFrame, col_point: str, col_date: str):
    """
    Generate Stiff diagrams for visualizing the ionic composition of water samples.

    This function creates Stiff diagrams for each unique sampling point and date in the dataset.
    A Stiff diagram is a polygonal chart used to represent the concentrations of major cations
    (e.g., calcium, magnesium, sodium + potassium) and anions (e.g., chlorides, sulfates, bicarbonates + carbonates)
    in water samples. The diagram helps in comparing the ionic composition of different water samples.

    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame containing the water sample data, including the following columns with concentrations
        in milliequivalents per liter (meq/L):
        - 'Sodio (meq/L)'
        - 'Potasio (meq/L)'
        - 'Cloruros (meq/L)'
        - 'Calcio (meq/L)'
        - 'Bicarbonato (meq/L)'
        - 'Carbonato (meq/L)'
        - 'Magnesio (meq/L)'
        - 'Sulfatos (meq/L)'
        - 'Nitratos (meq/L)'
    col_point : str
        The name of the column that identifies the sampling points.
    col_date : str
        The name of the column that contains the sampling dates.

    Returns:
    --------
    figures : dict
        A dictionary where keys are sampling point identifiers and values are the corresponding Matplotlib
        Figure objects containing the Stiff diagrams.

    Notes:
    ------
    - The function groups the data by sampling point and date, generating a separate Stiff diagram for each group.
    - Each diagram plots cations on the left and anions on the right, with the concentration in milliequivalents
      per liter (meq/L) on the x-axis.
    - The function checks for multiple records at the same sampling point and date and provides a warning if found.
    """
    figures = {}
    for point_id, point_values in df.groupby([col_point]):
        point_id = point_id if not isinstance(point_id, tuple) else point_id[0]
        fig, ax = plt.subplots(figsize=(8, 10))
        height = 0
        max_value = 1
        y_label_data = []
        y_label_data_str = []
        date_groups = len(point_values.groupby([col_date]))
        figure_length = (date_groups * 3 + (date_groups - 1) * 2) + 1
        for date, values in point_values.groupby([col_date]):
            date = date if not isinstance(date, tuple) else date[0]
            if len(values) == 1:
                Na_K = [
                    -(abs(values["Sodio (meq/L)"]) + abs(values["Potasio (meq/L)"])),
                    3 + height,
                ]
                cl = [abs(values["Cloruros (meq/L)"]), 3 + height]
                Ca = [-abs(values["Calcio (meq/L)"]), 2 + height]
                HCO_CO = [
                    abs(values["Bicarbonato (meq/L)"])
                    + abs(values["Carbonato (meq/L)"]),
                    2 + height,
                ]
                Mg = [-abs(values["Magnesio (meq/L)"]), 1 + height]
                SO4_NO3 = [
                    abs(values["Sulfatos (meq/L)"]) + abs(values["Nitratos (meq/L)"]),
                    1 + height,
                ]
                points = [Na_K, cl, HCO_CO, SO4_NO3, Mg, Ca]
                x = [point[0] for point in points]
                y = [point[1] for point in points]
                max_value = max([max([math.ceil(abs(val)) for val in x]), max_value])
                plt.fill(x, y, "blue", alpha=0.3)
                plt.scatter(x, y, marker=".", color="darkblue")
                y_label_data += [1 + height, 2 + height, 3 + height]
                y_label_data_str += ["Mg", "Na+K", "Ca"]
                height += 5
                label = point_id + "\n" + date.strftime("%Y-%m-%d")
                x_pos = -0.3
                y_pos = np.mean(y) / figure_length
                ax.text(
                    x_pos,
                    y_pos,
                    label,
                    horizontalalignment="right",
                    verticalalignment="center",
                    transform=ax.transAxes,
                )
            else:
                messagebox.showinfo(
                    "Alert Message",
                    f"The point {point_id} for the date {date.strftime('%Y-%m-%d')} has more than one record",
                )
        
        plt.xlim(-max_value, max_value)
        plt.ylim(0, max(y_label_data) + 1)
        interval = round(max_value * 2 / 10, 1)
        x_abs = [
            round(abs(val), 2) for val in np.arange(-max_value, max_value, interval)
        ]
        plt.xticks(np.arange(-max_value, max_value, interval), x_abs)
        plt.yticks(y_label_data, y_label_data_str)
        plt.xlabel("meq/L")
        ax.grid(linestyle="dashed", color="gray")
        _ = ax.twinx()
        plt.yticks(
            y_label_data, ["SO4+NO3", "HCO3+CO3", "Cl"] * int((len(y_label_data) / 3))
        )
        plt.xticks(np.arange(-max_value, max_value, interval), x_abs)
        plt.ylim(0, max(y_label_data) + 1)
        fig.tight_layout()
        figures[point_id] = fig
    return figures
