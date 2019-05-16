import json
import statistics
import matplotlib.pyplot as plt
import numpy as np

with open('accuracies.json', 'r') as fp:
    accuracies = json.load(fp)

# First let's plot average accuracy per compression type/no compression 
transformations = ["0", "2", "4", "8", "16"]
wordy_transformations = ["Original", "Frequency filtering", "Half bitrate", "Quarter bitrate", "1/8 bitrate"]
avg_acc = []
avg_acc_wo_zeros = []
zero_labels = []

t_dict = {}
order_labels = []

# determine which ones have 0 accuracies throughout
for key, accs in accuracies.items():
	if statistics.mean(accs.values()) == 0:
		zero_labels.append(key)
	else:
		order_labels.append(key)

for t in transformations:
	acc = []
	acc_no_zeros = []
	for key, accs in accuracies.items():
		acc.append(accs[t])
		if key not in zero_labels:
			acc_no_zeros.append(accs[t])
	t_dict[t] = acc_no_zeros
	avg_acc.append(statistics.mean(acc))
	avg_acc_wo_zeros.append(statistics.mean(acc_no_zeros))

print(avg_acc)
print(zero_labels)
print(avg_acc_wo_zeros)

# plt.bar(transformations, avg_acc)
# plt.ylim(top=1) 
# plt.suptitle('Average accuracy for all labels')
# plt.show()

# plt.bar(transformations, avg_acc_wo_zeros)
# plt.ylim(top=1) 
# plt.suptitle('Average accuracy excluding noisy labels')
# plt.show()

N = len(order_labels)
ind = np.arange(N)  # the x locations for the groups
width = 0.18      # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)

plt.rcParams.update({'font.size': 20,'font.sans-serif':'Arial'})
plt.rcParams.update({'axes.labelsize': 22})

colors = {
	'0': 'r',
	'2': 'g',
	'4': 'b',
	'8': 'orange',
	'16': 'cyan'
}
legends = []

for key, val in t_dict.items():
	rect = ax.bar(ind+width*(transformations.index(key)), val, width, color=colors[key])
	legends.append(rect[0])

ax.set_ylabel('Accuracy')
ax.set_xticks(ind+width)
ax.set_xticklabels(order_labels)
ax.legend(set(legends), set(wordy_transformations))

plt.suptitle('Accuracy per label')

plt.show()