import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
from matplotlib import patches
import matplotlib.font_manager as font_manager

# FIRST TASK


# I. Function for gff reading
def read_gff(input_gff):
    gff_dataframe = pd.read_csv(input_gff, sep='\t', header=1,
                                names=['chromosome', 'source', 'type', 'start',
                                       'end', 'score', 'strand', 'phase', 'attributes'])
    return gff_dataframe


# Function for bed reading
def read_bed6(input_bed):
    bed_dataframe = pd.read_csv(input_bed, sep='\t',
                                names=['chromosome', 'start', 'end', 'name', 'score', 'strand'])
    return bed_dataframe


rrana_dataframe = read_gff("rrna_annotation.gff")
alignment_dataframe = read_bed6("alignment.bed")


# II. Attribute simplification
# 1 step - replace unusual record
rrana_dataframe.attributes = rrana_dataframe.attributes.str.replace(r' \(partial.*', r'', regex=True)
# 2 step - substitute wist simple format
rrana_dataframe.attributes = rrana_dataframe.attributes.replace({'Name=23S_rRNA;product=23S ribosomal RNA': '23S',
                                                                 'Name=16S_rRNA;product=16S ribosomal RNA': '16S',
                                                                 'Name=5S_rRNA;product=5S ribosomal RNA': '5S'})

# III. Figure creation
# Replace reference on chromosome number
rrana_dataframe_double = rrana_dataframe
rrana_dataframe_double.chromosome = rrana_dataframe_double.chromosome.str.replace(r'(\w+_)', r'',
                                                                                  regex=True).astype('int64')
# Create table chromosome - rRNA content
rrana_dataframe_double.groupby('chromosome').aggregate({'attributes': 'value_counts'})

# Create plot
chromosome_count = rrana_dataframe_double.groupby('chromosome')['attributes'].value_counts()
chromosome_count.unstack(level=1).plot(kind='bar')
plt.title('rRNA barplot')
plt.legend(title="RNA type")
plt.ylabel('Count')
plt.xlabel('Chromosome')

# IV. Similar bedtools intersect
rrana_dataframe = read_gff("rrna_annotation.gff")
alignment_dataframe = read_bed6("alignment.bed")
rrana_dataframe.attributes = rrana_dataframe.attributes.str.replace(r' \(partial.*', r'', regex=True)
rrana_dataframe.attributes = rrana_dataframe.attributes.replace({'Name=23S_rRNA;product=23S ribosomal RNA': '23S',
                                                                 'Name=16S_rRNA;product=16S ribosomal RNA': '16S',
                                                                 'Name=5S_rRNA;product=5S ribosomal RNA': '5S'})
# Merge two dataframe
merged_data = rrana_dataframe.merge(alignment_dataframe, on=['chromosome'], suffixes=['_x', '_y'])
# Select suitable options
intersect_rrna_dataframe = merged_data.loc[(merged_data['start_y'] <= merged_data['start_x']) &
                                           (merged_data['end_y'] >= merged_data['end_x'])]

intersect_rrna_dataframe_modify = intersect_rrna_dataframe.drop('strand_y', inplace=True, axis=1)  # optionally

# SECOND TASK

# I. Preporation
dif_expr = pd.read_csv('/content/diffexpr_data.tsv.gz', sep='\t')

# II. Additional analysis


# Function for dividing gene expression on 4 groups
def significant(data_frame):
    if data_frame.logFC < 0 and data_frame.log_pval < .95:
        return 'Non-significantly downregelated'
    elif data_frame.logFC < 0 and data_frame.log_pval > .95:
        return 'Significantly downregelated'
    elif data_frame.logFC > 0 and data_frame.log_pval > .95:
        return 'Significantly upregelated'
    else:
        return 'Non-significantly upregelated'


dif_expr['Significance'] = dif_expr.apply(significant, axis=1)

# Limit determination
logFC_max = dif_expr.logFC.max() + 1
logFC_min = dif_expr.logFC.min() - 1
logFC_limit = max(abs(logFC_min), logFC_max)

# Select record gene
significant_dataframe = dif_expr.query('log_pval >= .95')
top2_downregulated = significant_dataframe.sort_values(by=['logFC']).head(2)
top2_upregulated = significant_dataframe.sort_values(by=['logFC'], ascending=False).head(2)
top2_together = pd.concat([top2_downregulated, top2_upregulated], axis=0)

# Create lists for annotation
record_genes = top2_together.Sample.tolist()
record_logFC = top2_together.logFC.tolist()
record_log_pval = top2_together.log_pval.tolist()

# Change settings rcParam
plt.rcParams['mathtext.fontset'] = 'dejavuserif'
plt.rcParams['mathtext.bf'] = 'italic:bold'
plt.rcParams['xtick.minor.visible'] = True
plt.rcParams['ytick.minor.visible'] = True
plt.rcParams['xtick.major.width']: 1
plt.rcParams['xtick.major.size']: 10
plt.rcParams['xtick.major.width']: 1
plt.rcParams['xtick.major.size']: 10
plt.rcParams['font.serif']: 'Times New Roman'

# III. Graphs
plt.figure(figsize=[10, 8], dpi=700)

# Creation of scatter plot
expr_graph = sns.scatterplot(data=dif_expr, x="logFC", y="log_pval",
                             hue='Significance',
                             hue_order=['Significantly downregelated', 'Significantly upregelated',
                                        'Non-significantly downregelated', 'Non-significantly upregelated'],
                             s=5, alpha=1, linewidth=0)

# Create horizontal threshold and label
expr_graph.axhline(y=0.95, color='grey', linewidth=1, linestyle='dashed')
plt.text(7, 1.6, 'p-value = 0.05', horizontalalignment='left', verticalalignment='center',
         color='grey', size=10, fontweight='bold')

# Create vertical threshold
expr_graph.axvline(x=0, color='grey', linewidth=1, linestyle='dashed')

# Adjust axis
plt.xlabel(r'$\bf {log_{2}}$(fold change)', fontweight='bold', fontstyle='italic', size=12)
plt.xticks(fontweight='bold', size=8)
plt.ylabel(r'-$\bf {log_{10}}$(p-value corrected)', fontweight='bold', fontstyle='italic', size=12)
plt.yticks(fontweight='bold', size=8)
plt.tick_params(which='major', width=1, size=5)
plt.setp(expr_graph.spines.values(), linewidth=1.3)

# Adjust limits
expr_graph.set_xlim(right=logFC_limit, left=-logFC_limit)
font = font_manager.FontProperties(weight='bold', size=8)

# Creation of legend
expr_graph.legend(prop=font, markerscale=1.2, shadow=True)

# Annotation of special genes
expr_graph.annotate(record_genes[0], xy=(record_logFC[0], record_log_pval[0]), xycoords='data',
                    xytext=(+10, +30), textcoords='offset points', fontsize=8, fontweight='bold',
                    arrowprops=dict(arrowstyle="simple", facecolor='red', edgecolor="black", lw=.25))
expr_graph.annotate(record_genes[1], xy=(record_logFC[1], record_log_pval[1]), xycoords='data',
                    xytext=(+10, +30), textcoords='offset points', fontsize=8, fontweight='bold',
                    arrowprops=dict(arrowstyle="simple", facecolor='red', edgecolor="black", lw=.25))
expr_graph.annotate(record_genes[2], xy=(record_logFC[2], record_log_pval[2]), xycoords='data',
                    xytext=(+10, +30), textcoords='offset points', fontsize=8, fontweight='bold',
                    arrowprops=dict(arrowstyle="simple", facecolor='red', edgecolor="black", lw=.25))
expr_graph.annotate(record_genes[3], xy=(record_logFC[3], record_log_pval[3]), xycoords='data',
                    xytext=(+15, +60), textcoords='offset points', fontsize=8, fontweight='bold',
                    arrowprops=dict(arrowstyle="simple", facecolor='red', edgecolor="black", lw=.25))
plt.title('Volcano plot', fontweight='bold', fontstyle='italic', size=16)
plt.savefig('Volcano_plot.png')

# THIRD TASK

# I. Preparation
cancer_data = pd.read_csv('Worldwide Cancer Dataset.csv')
cancer_data = cancer_data.rename(columns={'Rank': 'Rank', 'Cancer': 'Cancer',
                                          'New cases in 2020': 'New', '% of all cancers': 'Percent'})
cancer_data['New'] = cancer_data['New'].str.replace(',', '')    # incorrect record
cancer_data = cancer_data.drop([0])                             # delete total row

# Divide into two group
major_cancer = cancer_data.query('Percent >= 3')
other_cancer = cancer_data.query('Percent < 3')

# Recalculate percent of minor fraction
other_cancer['New'].astype(int).sum()                                   # =4311828
other_cancer['New'] = other_cancer['New'].astype(int)
other_cancer['Percent'] = other_cancer.apply(lambda row: row.New / 4311828, axis=1)
major_cancer.loc[len(major_cancer)] = [12.0, 'Other', 4311828, 23.8]    # add row for other types in major
ratio = major_cancer.Percent.tolist()
explode = [0]*(len(major_cancer)-1) + [0.1]

# II. Short analysis
ratio = major_cancer['Percent'].tolist()
cancer = major_cancer['Cancer'].tolist()
other_ratio = other_cancer['Percent'].tolist()
other_label = other_cancer['Cancer'].tolist()

III. Graph
# Creation of figure
distrib, (part1, part2) = plt.subplots(1, 2, figsize=(18, 11), dpi=300)
distrib.subplots_adjust(wspace=0)

# Pie chart
explode = [0] * (len(major_cancer) - 1) + [0.11]
angle = 90 * ratio[0]
colors = sns.color_palette("husl")[0:11]
wedges, *_ = part1.pie(ratio, startangle=angle, explode=explode, colors=colors)

# Bar plot
bottom = 1
width = 0.2
start = 0
for j in range(len(other_ratio)):
    height = other_ratio[j]
    part2.bar(start, height, width, bottom=bottom)
    grow = bottom + part2.patches[j].get_height() / 2
    bottom += height

part2.axis('off')
part2.set_xlim(-2.5 * width, 2.5 * width)

# Draw lines between the two plots
theta1, theta2 = wedges[10].theta1, wedges[10].theta2
center, r = wedges[10].center, wedges[10].r
bar_height = sum(other_ratio)

# Top line
x = r * np.cos(np.pi / 180 * theta2) + center[0]
y = r * np.sin(np.pi / 180 * theta2) + center[1]
con = ConnectionPatch(xyA=(-width / 2, bar_height * 2), coordsA=part2.transData,
                      xyB=(x, y), coordsB=part1.transData)
con.set_color([0, 0, 0])
con.set_linewidth(1)
part2.add_artist(con)

# Bottom line
x = r * np.cos(np.pi / 180 * theta1) + center[0]
y = r * np.sin(np.pi / 180 * theta1) + center[1]
con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=part2.transData,
                      xyB=(x, y), coordsB=part1.transData)
con.set_color([0, 0, 0])
part2.add_artist(con)
con.set_linewidth(1)

# Pie annotation
bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
kw = dict(arrowprops=dict(arrowstyle="-"),
          bbox=bbox_props, zorder=0, va="center")

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1) / 2. + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    connectionstyle = "angle,angleA=0,angleB={}".format(ang)
    kw["arrowprops"].update({"connectionstyle": connectionstyle})
    part1.annotate(s=f'{cancer[i]}\n {ratio[i]}%', xy=(x, y), xytext=(1.8 * np.sign(x), 1.8 * y),
                   fontsize=8, horizontalalignment='center', **kw)

# Bar annotation
bottom = 1
x = 0.2

for i in range(7):
    y = bottom + other_ratio[i] / 2
    bottom += other_ratio[i]
    part2.annotate(s=f'{other_label[i]}\n {"%.1f" % (other_ratio[i] * 100)}%', xy=(x, y), xycoords='data',
                   xytext=(+15, -5), textcoords='offset points', fontsize=8, horizontalalignment='center',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', lw=2))

plt.savefig('Pie_plot.png')
