
from matplotlib_venn import venn3
import matplotlib.pyplot as plt

# Define the sets
fields_info = {"Data Science", "Information\nSystem", "Artificial\nIntelligence", "Cybernetics (A)", "Informatics (I)", "Smart System (C)"}
fields_ctrl = {"System\nEngineering", "Mechatronics", "Artificial\nIntelligence", "Cybernetics (A)", "Informatics (I)", "Smart System (C)"}
fields_auto = {"Robotics", "Mechatronics", "Information\nSystem", "Cybernetics (A)", "Informatics (I)", "Smart System (C)"}

# Create the Venn diagram
venn = venn3([fields_info, fields_ctrl, fields_auto],
             ('Information', 'Control', 'Automation'))

# Define subset labels
subsets = {
    '100': fields_info - fields_ctrl - fields_auto,
    '010': fields_ctrl - fields_info - fields_auto,
    '001': fields_auto - fields_info - fields_ctrl,
    '110': fields_info & fields_ctrl - fields_auto,
    '101': fields_info & fields_auto - fields_ctrl,
    '011': fields_ctrl & fields_auto - fields_info,
    '111': fields_info & fields_ctrl & fields_auto,
}

# Update the labels for each subset
for subset_id, elements in subsets.items():
    label = venn.get_label_by_id(subset_id)
    if label:  # Check if the subset exists
        label.set_text("\n".join(elements))  # Set the new label text

# Display the plot
plt.show()
