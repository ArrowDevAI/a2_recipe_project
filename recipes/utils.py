from io import BytesIO 
import base64
import matplotlib.pyplot as plt

def get_graph():
   buffer = BytesIO()         
   plt.savefig(buffer, format='png')

   buffer.seek(0)

   image_png=buffer.getvalue()

   graph=base64.b64encode(image_png)

   graph=graph.decode('utf-8')

   buffer.close()

   return graph
def get_chart(chart_type, data, **kwargs):
    # Switch plot backend to AGG (Anti-Grain Geometry) - to write to file
    plt.switch_backend('AGG')

    # Specify figure size
    fig = plt.figure(figsize=(6, 3))

    # Select chart_type based on user input from the form
    if chart_type == '#1':
        # Bar chart between name and cook_time
        plt.bar(data['name'], data['cook_time'])
        plt.xlabel('Recipe Name')  # Label for x-axis
        plt.ylabel('Cook Time (minutes)')  # Label for y-axis
        plt.title('Cook Time by Recipe Name')  # Chart title

    elif chart_type == '#2':
        # Pie chart for difficulty distribution
        difficulty_counts = data['difficulty'].value_counts()
        labels = difficulty_counts.index.tolist()
        plt.pie(difficulty_counts, labels=labels, autopct='%1.1f%%')
        plt.title('Difficulty Distribution')  # Chart title

    elif chart_type == '#3':
        # Line chart (could be cook_time vs name as an example)
        plt.plot(data['name'], data['cook_time'])
        plt.xlabel('Recipe Name')  # Label for x-axis
        plt.ylabel('Cook Time (minutes)')  # Label for y-axis
        plt.title('Cook Time by Recipe Name (Line Chart)')  # Chart title

    else:
        print('Unknown chart type')

    # Specify layout details
    plt.tight_layout()

    # Render the graph to file
    chart = get_graph() 
    return chart
