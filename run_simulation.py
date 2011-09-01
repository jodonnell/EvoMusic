import evolution
import cPickle

def dump_progress(data, generation_num):
    compare_file = open('test_data/compare%d' % generation_num, 'w')
    cPickle.dump(data, compare_file, 2)

RECORD_ON = [0, 1, 2, 3, 5, 10, 25, 50, 75, 100, 200, 500, 700, 900, 999]
for i in range(1000, 50000, 1000):
    RECORD_ON.append(i)
print RECORD_ON

NUM_ITERATIONS = 10000

sampling_info = evolution.get_sampling('annie.wav')
evolution.convert_to_unsigned_int(sampling_info)
selection_sampling = evolution.NaturalSelector(sampling_info) # pass in data
gene_pool = evolution.OrganismPool(selection_sampling)

#for i in range(NUM_ITERATIONS):

#    top_organism = gene_pool.new_generation()
#    print top_organism.fitness
#    if (i % 100) == 0:
#        print i

#    if (i in RECORD_ON) :
#        dump_progress(top_organism.get_organism_chromosomes(), i)
        #play_sound(gene.get_gene_data())


base_file = open('test_data/base', 'w')
cPickle.dump(sampling_info, base_file, 2)

