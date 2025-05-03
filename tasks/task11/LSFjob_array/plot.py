import matplotlib.pyplot as plt

real_times = [8.88, 15.31, 19.43, 20.23, 11.30, 13.14, 11.24, 12.75, 10.17, 16.09, 15.93, 9.78, 16.81, 14.60, 15.20, 10.02, 11.85, 10.96, 10.72, 16.59, 16.07, 11.96, 14.27, 14.47]


plt.figure(figsize=(10, 6))
plt.bar(range(len(real_times)), real_times)
plt.ylabel('Time (minutes)')
plt.xlabel('job index')
plt.xticks(range(len(real_times)), range(1, len(real_times)+1))

plt.savefig('time_chart.png', dpi=300, bbox_inches='tight')
plt.close()

