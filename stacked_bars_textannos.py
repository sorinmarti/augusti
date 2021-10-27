import csv

from bokeh.core.property.dataspec import value
from bokeh.io import output_file
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show


def get_categories(bit):
    cats = list()
    if 'Abkürzungsauflösung' in bit:
        cats.append('AA')
    if 'Ergänzung' in bit:
        cats.append('ER')
    if 'Korrektur' in bit:
        cats.append('KO')
    if 'Wortwiederholung' in bit:
        cats.append('WW')
    if 'Nicht lesbar' in bit:
        cats.append('NL')
    if bit == '':
        cats.append('BL')
    return cats


def read_csv():
    with open('./annos.tsv', encoding='utf8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter='\t')
        line_count = 0
        csv_data = list()
        for row in csv_reader:
            if line_count == 0:
                # Ignore title line
                line_count += 1
            else:
                if 'Textannotation' in row[9]:
                    print("READ: Found Textannotation")
                    if 'v' in row[4]:
                        page_number = int(row[4].replace('v', ''))*2
                    elif 'r' in row[4]:
                        page_number = int(row[4].replace('r', ''))*2 - 1
                    else:
                        page_number = 0

                    if page_number != 0:
                        page_number = page_number - 188

                    line_dict = {'anno-id': row[0],
                                 'page': row[4],
                                 'page-number': page_number,
                                 'categories': get_categories(row[10])}
                    csv_data.append(line_dict)
                    print("READ: Line added")
                    print(line_dict)
                    line_count += 1

        return csv_data


def get_structured_data():
    my_data = read_csv()
    aa_list = [0] * 104
    bl_list = [0] * 104
    ko_list = [0] * 104
    er_list = [0] * 104
    nl_list = [0] * 104
    ww_list = [0] * 104

    amb_list = [0] * 104
    pages_list = []
    p_number = 94
    for i in range(104):
        if i%2 == 0:
            p_number += 1
            page_str = str(p_number) + 'r'
        else:
            page_str = str(p_number) + 'v'

        pages_list.append(page_str)

    for data_point in my_data:
        print("STRUCTURE:", data_point)
        if len(data_point['categories']) > 1:
            amb_list[data_point['page-number']-1] += 1
        elif len(data_point['categories']) == 0:
            pass
        else:
            if data_point['categories'][0] == 'AA':
                aa_list[data_point['page-number']-1] += 1
            if data_point['categories'][0] == 'BL':
                bl_list[data_point['page-number']-1] += 1
            if data_point['categories'][0] == 'KO':
                ko_list[data_point['page-number']-1] += 1
            if data_point['categories'][0] == 'ER':
                er_list[data_point['page-number']-1] += 1
            if data_point['categories'][0] == 'NL':
                nl_list[data_point['page-number']-1] += 1
            if data_point['categories'][0] == 'WW':
                ww_list[data_point['page-number']-1] += 1

    extracted_data = {'pages': pages_list,
                      'AA': aa_list,
                      'KO': ko_list,
                      'ER': er_list,
                      'BL': bl_list,
                      'NL': nl_list,
                      'WW': ww_list,
                      'AMB': amb_list}

    return pages_list, extracted_data, ["AA", "KO", "ER", "NL", "WW", "BL", "AMB"], \
           ["Abkürzungsauflösung", "Korrektur", "Ergänzung", "Nicht lesbar", "Wortwiederholung", "Blank", "Mehrere"]


output_file("stacked.html")
pages, data, categories, cat_labels = get_structured_data()
print(pages)
p = figure(x_range=pages, title="Category Count By Page", width=2000)

colors = ["#F1948A", "#7FB3D5", "#82E0AA", "#C39BD3", "#73C6B6", "#F8C471", "#B2BABB"]
p.vbar_stack(categories, x='pages', width=.9, color=colors, source=data, legend=[value(x) for x in cat_labels])

p.y_range.start = 0
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_right"
p.legend.orientation = "vertical"

p = gridplot([[p]], sizing_mode='stretch_both')
show(p)
show(p)
