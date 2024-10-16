import numpy as np
from matplotlib import pyplot as plt


def create_horizontal_bar_chart_with_annotations(dictionary, category_colors):
    plt.figure(figsize=(5, 8))

    category_names = list(dictionary.keys())
    category_positions = (
        []
    )  # To track y-position of each category for labeling
    current_position = 0  # Current y position for plotting bars

    for category, elements_dict in dictionary.items():
        # Check if the category is "Monomers" to decide the number of elements to display
        if category == "Monomers":
            sorted_elements = dict(
                sorted(
                    elements_dict.items(),
                    key=lambda item: item[1],
                    reverse=False,
                )
            )
        else:
            sorted_elements = dict(
                sorted(
                    elements_dict.items(),
                    key=lambda item: item[1],
                    reverse=False,
                )[-5:]
            )

        max_value = max(
            sorted_elements.values()
        )  # Find the maximum value for normalization
        names = list(sorted_elements.keys())
        values = [value / max_value for value in sorted_elements.values()]

        # Plot bars for this category
        y_positions = np.arange(
            current_position, current_position + len(names)
        )
        plt.barh(
            y_positions * 4,
            values,
            height=3.8,
            color=category_colors[category],
            label=category.capitalize(),
            edgecolor='black',
            alpha=0.5,
        )
        # Annotate each bar with its element name
        for y, name in zip(y_positions * 4, names):
            plt.text(
                0.01, #values[names.index(name)] - 0.05,
                y,
                name,
                ha='left',
                va='center',
                fontsize=8,
            )

        # Update for next category
        category_positions.append(np.mean(y_positions * 4))
        current_position += (
            len(names) + 1
        )  # Adding 1 for gap between categories

    # Labeling categories
    plt.yticks(category_positions, category_names, fontsize=12)

    # Adding labels and title
    plt.xlabel('Normalized Frequency', fontsize=14)
    # plt.savefig('literature_receipt_figure_horizontal_customized.svg')
    plt.show()
