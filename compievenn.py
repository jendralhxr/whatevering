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
