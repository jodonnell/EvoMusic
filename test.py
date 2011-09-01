import anaylze_performance


RECORD_ON = [0, 1, 2, 3, 5, 10, 25, 50, 75, 100]
for i in range(1000, 10000, 1000):
    RECORD_ON.append(i)

for i in RECORD_ON:
    print str(i) + ": " + str(anaylze_performance.compare_results('test_data/base', 'test_data/compare%d' % i))
