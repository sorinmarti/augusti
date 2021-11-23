import csv
import matplotlib.pyplot as plt
import wordcloud
from matplotlib import cm
from wordcloud import WordCloud


# Define a function to plot word cloud
def plot_cloud(wordcloud, filename=None):
    plt.imshow(wordcloud)
    plt.axis("off")
    if filename:
        wordcloud.to_file(filename)
        plt.clf()
    else:
        plt.show()


# Update Stopwords for WordCloud
wordcloud.STOPWORDS.update(["der", "die", "das", "des", "er", "dem", "den", "und", "oder", "ein", "eine",
                            "sie", "seiner", "Du", "zu", "auf", "als", "für", "von", "zum", "wir"])
wordcloud.STOPWORDS.update(["nec", "ut", "et"])


def get_row_tuple(row: list):
    ret_value = {"id": row[0],
                 "words": row[1],
                 "metaphor": row[2],
                 "orig": row[3],
                 "pro_stauffer": True if row[5] != '' else False,
                 "anti_stauffer": True if row[6] != '' else False,
                 "pos_moral": True if row[7] != '' else False,
                 "neg_moral": True if row[8] != '' else False,
                 "folio": row[9],
                 "row": row[10],
                 "page": int(row[9].replace("v", ""))}

    try:
        ret_value["row_int"] = int(row[10])
    except ValueError:
        ret_value["row_int"] = 0
    return ret_value


def read_file(filename):
    list_of_actors = {}
    list_of_pages = {}

    with open(filename, encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='\t')
        count = 0
        highest_page = 0
        lowest_page = 9999
        for row in csv_reader:
            if count == 0:
                count += 1
                print(f"Skipped first row.")
            else:
                # Actor must be set
                if row[4] != '' and row[9] != '':
                    row_tuple = get_row_tuple(row)
                    if row_tuple["page"] > highest_page:
                        highest_page = row_tuple["page"]

                    if row_tuple["page"] < lowest_page:
                        lowest_page = row_tuple["page"]

                    if row[4] not in list_of_actors:
                        list_of_actors[row[4]] = list()
                    list_of_actors[row[4]].append(row_tuple)

                    if row[9] not in list_of_pages:
                        list_of_pages[row[9]] = list()
                    list_of_pages[row[9]].append(row_tuple)
                else:
                    print(f"Skipped row '{'//'.join(row)}' because actor is empty.")

    for actor in list_of_actors:
        list_of_actors[actor] = sorted(list_of_actors[actor], key=lambda d: d['row_int'])

    return list_of_actors, list_of_pages, lowest_page, highest_page


actors, pages, lowest, highest = read_file('sprache.tsv')
page_range = (highest - lowest) + 1

print(actors["Konrad v. Querfurt"])

for a in actors:
    fn = a.replace(" ", "").replace(".", "").replace("/", "")
    lat_text_list = list()
    ger_text_list = list()
    ger_text_list_2 = list()
    merged_ger_text_list = list()

    for row_tuple in actors[a]:
        lat_text_list.append(row_tuple["orig"])
        ger_text_list.append(row_tuple["words"])
        ger_text_list_2.append(row_tuple["metaphor"])
        merged_ger_text_list.append(row_tuple["words"] + " " + row_tuple["metaphor"])

    lat_wordcloud = WordCloud().generate(" ".join(lat_text_list))
    plot_cloud(lat_wordcloud, filename=f'wordclouds/orig/{fn}.png')

    ger_wordcloud = WordCloud().generate(" ".join(ger_text_list))
    plot_cloud(ger_wordcloud, filename=f'wordclouds/words/{fn}.png')

    ger_2_wordcloud = WordCloud().generate(" ".join(ger_text_list_2))
    plot_cloud(ger_2_wordcloud, filename=f'wordclouds/metaphors/{fn}.png')

    merged_ger_wordcloud = WordCloud().generate(" ".join(merged_ger_text_list))
    plot_cloud(merged_ger_wordcloud, filename=f'wordclouds/words_metaphors/{fn}.png')


fig, ax = plt.subplots()

for a in actors:
    pop_index_on_page = [0] * page_range
    for line in actors[a]:
        array_index = line["page"] - lowest

        if line["pro_stauffer"]:
            pop_index_on_page[array_index] += 1
        if line["anti_stauffer"]:
            pop_index_on_page[array_index] -= 1
        if line["pos_moral"]:
            pop_index_on_page[array_index] += 1
        if line["neg_moral"]:
            pop_index_on_page[array_index] -= 1

        if array_index > 0:
            for x in range(array_index, page_range):
                pop_index_on_page[x] = pop_index_on_page[array_index]

    print(a, pop_index_on_page)
    ax.plot(range(page_range), pop_index_on_page)
    ax.set_ylabel(a)

ax.set_xlabel("Folio")
ax.set_ylabel("Popularity Index")
plt.xticks(range(0, page_range, 5), range(lowest, highest+1, 5))
plt.legend(actors.keys(), loc='upper left')
plt.savefig('popularity_index.png')
# plt.show()
plt.clf()

for a in actors:
    fn = a.replace(" ", "").replace(".", "").replace("/", "")
    pos_index_on_page = [0] * page_range
    neg_index_on_page = [0] * page_range
    pro_index_on_page = [0] * page_range
    anti_index_on_page = [0] * page_range
    for line in actors[a]:
        array_index = line["page"] - lowest

        if line["pro_stauffer"]:
            pro_index_on_page[array_index] += 1
        if line["anti_stauffer"]:
            anti_index_on_page[array_index] -= 1
        if line["pos_moral"]:
            pos_index_on_page[array_index] += 1
        if line["neg_moral"]:
            neg_index_on_page[array_index] -= 1

        if array_index > 0:
            for x in range(array_index, page_range):
                neg_index_on_page[x] = neg_index_on_page[array_index]
                pos_index_on_page[x] = pos_index_on_page[array_index]
                pro_index_on_page[x] = neg_index_on_page[array_index]
                anti_index_on_page[x] = pos_index_on_page[array_index]

    fig, ax = plt.subplots()
    ax.plot(range(page_range), pro_index_on_page)
    ax.plot(range(page_range), anti_index_on_page)
    ax.plot(range(page_range), pos_index_on_page)
    ax.plot(range(page_range), neg_index_on_page)
    ax.set_ylabel("Neg")
    ax.set_xlabel("Folio")
    ax.set_ylabel("Weighed Mentions")
    plt.title(a)
    plt.xticks(range(0, page_range, 5), range(lowest, highest + 1, 5))
    plt.legend(["pro stauffisch", "anti-stauffisch",
                "moralisch positiv", "moralisch negativ"], loc='upper left')
    plt.savefig(f'pop/{fn}.png')
    plt.clf()


for a in actors:
    fn = a.replace(" ", "").replace(".", "").replace("/", "")
    x_pro_anti = [0] * page_range
    y_pos_neg = [0] * page_range

    for line in actors[a]:
        array_index = line["page"] - lowest
        if line["pro_stauffer"]:
            x_pro_anti[array_index] += 1
        if line["anti_stauffer"]:
            x_pro_anti[array_index] -= 1
        if line["pos_moral"]:
            y_pos_neg[array_index] += 1
        if line["neg_moral"]:
            y_pos_neg[array_index] -= 1

    plt.figure()
    # Hold activation for multiple lines on same graph
    # plt.hold('on')
    # Set x-axis range
    plt.xlim((-30,30))
    # Set y-axis range
    plt.ylim((-30,30))
    # Draw lines to split quadrants
    plt.plot([-30,30],[0,0], linewidth=1, color='red' )
    plt.plot([0,0],[30,-30], linewidth=1, color='red' )
    plt.title(a)
    # Draw some sub-regions in upper left quadrant
    # plt.plot([3,3],[5,9], linewidth=2, color='blue')
    # plt.plot([1,5],[7,7], linewidth=2, color='blue')

    plt.plot(x_pro_anti, y_pos_neg, linewidth=1)
    plt.savefig(f'quad/{fn}.png')
    plt.clf()
