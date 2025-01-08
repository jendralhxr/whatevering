from matplotlib_venn import venn3
import matplotlib.pyplot as plt

# Define the sets
fields_info = {"Data Science", "Information Systems", "Artificial Intelligence", "Cybernetics"}
fields_ctrl = {"System Engineering", "Mechatronics", "Artificial Intelligence", "Cybernetics"}
fields_auto = {"Robotics", "Mechatronics", "Information System", "Cybernetics"}

# Create the Venn diagram
venn = venn3([fields_info, fields_ctrl, fields_auto],
             ('Information', 'Control', 'Automation'))

# Add annotations to specific overlaps
venn.get_label_by_id('100').set_text('Data\nScience')
venn.get_label_by_id('010').set_text('System\nEngineering')
venn.get_label_by_id('001').set_text('Robotics')
venn.get_label_by_id('110').set_text('Artificial\nIntelligence')
venn.get_label_by_id('101').set_text('Information\nSystem')
venn.get_label_by_id('011').set_text('Mechatronics')
venn.get_label_by_id('111').set_text('Cybernetics')

# Add a title and display the plot
plt.title("Computer-Related Fields Based on Utilization Purpose", fontsize=12)
plt.show()


#####

import matplotlib.pyplot as plt

# Create the figure and axis
fig, ax = plt.subplots(figsize=(8, 8))

# Define circle colors
circle_colors = ['skyblue', 'lightgreen', 'orange', 'lightpink']

# Manually position the circles and create the labels
circles = [
    plt.Circle((-0.5, 0.5), 0.4, color=circle_colors[0], alpha=0.5),  # Set 1: Information
    plt.Circle((0.5, 0.5), 0.4, color=circle_colors[1], alpha=0.5),   # Set 2: Control
    plt.Circle((0.5, -0.5), 0.4, color=circle_colors[2], alpha=0.5),  # Set 3: Automation
    plt.Circle((-0.5, -0.5), 0.4, color=circle_colors[3], alpha=0.5)   # Set 4: Entertainment
]

# Add circles to the plot
for circle in circles:
    ax.add_patch(circle)

# Place the set labels at appropriate positions
ax.text(-0.5, 0.8, 'Information', ha='center', va='center', fontsize=12, color='black')
ax.text(0.5, 0.8, 'Control', ha='center', va='center', fontsize=12, color='black')
ax.text(0.5, -0.8, 'Automation', ha='center', va='center', fontsize=12, color='black')
ax.text(-0.5, -0.8, 'Entertainment', ha='center', va='center', fontsize=12, color='black')

# Define a custom function for handling the label text in each area
def place_text(positions, labels):
    for position, label in zip(positions, labels):
        ax.text(position[0], position[1], label, ha='center', va='center', fontsize=10)

# Define some sample positions for the intersections and their corresponding labels
intersection_positions = [
    (-0.4, 0.6),  (0.6, 0.6),  (0.6, -0.6), (-0.4, -0.6),  # Corner intersections
    (-0.2, 0),    (0.2, 0),     (0, -0.2),                 # Middle intersections
]
intersection_labels = [
    'Data Science\nAI', 'Gaming\nMedia', 'Robotics\nCybernetics', 'System Engineering\nMechatronics',
    'Artificial Intelligence\nInformation System', 'Mechatronics\nVirtual Reality', 'Cybernetics\nEntertainment'
]

# Place the intersection labels on the plot
place_text(intersection_positions, intersection_labels)

# Set the plot's limits and remove axis labels
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_aspect('equal')
ax.axis('off')  # Hide axes

# Add a smaller title
plt.title("Intersections of Computer-Related Fields and Entertainment", fontsize=12)

# Display the plot
plt.show()
