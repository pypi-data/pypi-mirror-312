from bokeh.io import curdoc
from bokeh.layouts import column, row
import bokeh.models
from bokeh.models.widgets import Paragraph


from stardiceonline.tools.metadatamanager import MetaDataManager
from stardiceonline.tools import orgfiles
from stardiceonline.tools.datesandtimes import utctime

manager = MetaDataManager()

targets, _ = orgfiles.fromorg(manager.get_data('targets.org', 'http://supernovae.in2p3.fr/stardice/stardiceot1/targets.org'))

# Sample data
target_list = list(targets['TARGET'])

# Sample data
data = dict(targets=[], times=[])
source = bokeh.models.ColumnDataSource(data)

# Define columns for the DataTable
columns = [
    bokeh.models.TableColumn(field="targets", title="Target"),
    bokeh.models.TableColumn(field="times", title="Time (UTC)", formatter=bokeh.models.DateFormatter(format='%FT%H:%M'))
]

# Create the DataTable with selection enabled
data_table = bokeh.models.DataTable(source=source, columns=columns, editable=False, width=600, index_position=None, selectable=True)

# Function to add a new row
def add_row():
    print(new_time.value)
    new_data = {'targets': [new_target.value], 'times': [utctime(new_time.value.hour, new_time.value.minute)]}
    source.stream(new_data)

# Function to modify the selected row
def modify_row():
    selected_row = source.selected.indices
    if selected_row:
        index = selected_row[0]
        source.patch({
            'targets': [(index, new_target.value)],
            'times': [(index, utctime(new_time.value.hour, new_time.value.minute))]
        })
    else:
        print("No row selected")

# Function to delete the selected row
def delete_row():
    selected_row = source.selected.indices
    if selected_row:
        index = selected_row[0]
        data = dict(source.data)
        for key in data:
            data[key].pop(index)
        source.data = data
    else:
        print("No row selected")

# Callback for when data changes
def update(attr, old, new):
    print("Table Updated:", source.data)

def change_selection(attr, old_indices, new_indices):
    if new_indices:
        selected_time = source.data['times'][new_indices[0]]
        selected_target = source.data['targets'][new_indices[0]]
        new_target.value = selected_target
        new_time.value = selected_time.time()
        
source.on_change('data', update)
source.selected.on_change('indices', change_selection)
# Input widgets for adding/modifying row
new_target = bokeh.models.Select(title="Target:", value="G191B2B", options=target_list)
#new_target = TextInput(title="Target:", value="")
new_time = bokeh.models.TimePicker(title="Time (UTC):", value=utctime().time())

# Buttons for table operations
add_button = bokeh.models.Button(label="Add Row", )
modify_button = bokeh.models.Button(label="Modify Row")
delete_button = bokeh.models.Button(label="Delete Row")
check = bokeh.models.Button(label='Check program and upload', button_type="success")

add_button.on_click(add_row)
modify_button.on_click(modify_row)
delete_button.on_click(delete_row)

# Feedback widget
feedback = Paragraph(text="")

# Layout
control_row =row(new_target, new_time,  column(row(add_button, modify_button, delete_button),
                                               check))
                     
layout = column(control_row, data_table, feedback, name="my_table")

# Add to current document
curdoc().add_root(layout)
curdoc().title = "Observation program"
