# See: http://www.relisoft.com/science/Physics/sampling.html
# http://pymedia.org/tut/dump_wav.html

# Get song clip
# Create a bunch of genes starting with random values (16 bit numbers)
# randomly change values (mutate) for each gene
# compare to source song and rate its mutation
# take top mutations and use them as the starting values for next generation


# worried that the thing will max out and over time changes will do more hurt than good

# Gene pool Class
# contains a list of genes initalized randomly
#

# TODO:
#   Breeding
#   Threading
#   Testing performance

from random import randint

MIN_SAMPLE_INT = -32767
MAX_SAMPLE_INT = 32767

MAX_ADJUSTED_SAMPLE_INT = MAX_SAMPLE_INT * 2 + 1
def random_gene_value():
    return randint(0, MAX_ADJUSTED_SAMPLE_INT)


class NaturalSelector(object):
    """This is the class that holds the target sound sampling
    It is what models the Natural Selection process
    The genes compare themselves to the data this holds, things
    that are close to this have a higher chance of surviving
    and mutating
    """

    def __init__(self, ideal_organism):
        self.ideal_organism = ideal_organism
        self.NUM_CHROMOSOMES = len(ideal_organism)

    def compare(self, organisms_value, chromosome, gene):
        "Lower is better, 0 is ideal and means the organism has the ideal gene"
        ideal_value = self.ideal_organism[chromosome][gene]
        return abs(ideal_value - organisms_value)
        
        
    
class Organism(object):
    """Represents a sound sampling that has been generated based off iterations
    It can create a random sound sampling, otherwise its only function is to
    mutate and assign a score to the effectiveness of its mutation
    """
    NUM_MUTATIONS = 20
    
    def __init__(self, natural_selector):
        self.natural_selector = natural_selector
        self._create_random()
        self.set_fitness()

    def _create_random(self):
        self.chromosomes = []
        for i in range(self.natural_selector.NUM_CHROMOSOMES):
            self.chromosomes.append([random_gene_value(), random_gene_value()])

    def set_fitness(self):
        """Fitness is defined by closest to the natural selector(the starting sound clip we are trying to reproduce)
        The lower the fitness the better, 0 would mean they match exactly
        """
        fitness_total = 0
        for chromosome in range(self.natural_selector.NUM_CHROMOSOMES):
            for gene in (0, 1):
                organism_value = self.chromosomes[chromosome][gene]

                fitness = self.natural_selector.compare(organism_value, chromosome, gene)
                fitness_total += fitness

        self.fitness = fitness_total
        

    def mutate(self):
        """
        OK so this badboy takes the original array and makes some random changes.
        Mutations keep the organism from plateauing.  In some cases for an organism
        to evolve to a better form, they need to take some steps backward. Also once
        in a blue moon a random mutation is beneficial
        """
        for i in range(self.NUM_MUTATIONS):
            random_gene = randint(0, 1)
            random_chromosome = randint(0, self.natural_selector.NUM_CHROMOSOMES - 1)

            new_gene_value = random_gene_value()

            add_or_subtract = randint(0, 1)
            mutation_amount = randint(1, 5)
            if add_or_subtract:
                self.chromosomes[random_chromosome][random_gene] = self.chromosomes[random_chromosome][random_gene] + mutation_amount
            else:
                self.chromosomes[random_chromosome][random_gene] = self.chromosomes[random_chromosome][random_gene] - mutation_amount
            
    def get_chromosome(self, chromosome):
        return self.chromosomes[chromosome]

    def get_organism_chromosomes(self):
        return self.chromosomes

    def set_chromosome(self, chromosome, gene1, gene2):
        self.chromosomes[chromosome] = [gene1, gene2]

# create random start

# on new_generation
# breed top 10
#   number 1 breeds with 2-10
#   number 2 with 3-10... until 50 are filled
#   breeding consists of looping through chromosome and taking gene(left and right channels are genes) from random parent
#   apply random mutation to random gene on random chromosome for each organism
# find top 10
#   look at every element and determine its rating
#   sort organisms
# new_generation should return top organism

# new terminology 
# GenePool -> OrganismPool
# Gene -> Organism
# SelectionSampling -> NaturalSelector

class OrganismPool(object):
    """Contains a pool of organisms, each of the organisms in the pool breed, and mutate somewhat.
    They are then compared to the natural selector.  The organisms are then compared to find the most
    successful organisms, these are bred and their children will repeat the process.
    """
    NUM_SURVIVORS = 15
    ORGANISM_POOL_SIZE = 70

    def __init__(self, natural_selector):
        "Creates a new organism pool and creates a random set of staring organisms and orders them by fitness"
        self.organisms = []
        self.natural_selector = natural_selector
        
        for i in range(self.ORGANISM_POOL_SIZE):
            organism = Organism( natural_selector )
            self.organisms.append(organism)

        self._order_by_fitness()

    def new_generation(self):
        """Breeds, mutates, and orders the current generation, finds the best of the best and repopulates the 
        organism pool as children of these top dogs, returns the fittest organism of the generation
        """
        self._breed_fittest_organisms()
        self._mutate_organism_pool()
        self._set_pool_fitness()
        self._order_by_fitness()
        return self.organisms[0]

    def _breed_fittest_organisms(self):
        fittest_organisms = self.organisms[ :self.NUM_SURVIVORS ]
        breeding_list = self._get_breeding_list()

        for breed in breeding_list:
            self._breed(self.organisms[breed['survivor']], self.organisms[breed['breed_with']], self.organisms[breed['organism_to_kill']])
            
    def _get_breeding_list(self):
        organism_to_kill = self.NUM_SURVIVORS
        breeding_list = []
        for survivor in range(self.NUM_SURVIVORS):
            for breed_with in range(survivor + 1, self.NUM_SURVIVORS):
                breeding_list.append({'survivor':survivor, 'breed_with':breed_with, 'organism_to_kill':organism_to_kill})
                organism_to_kill += 1

                if organism_to_kill >= self.ORGANISM_POOL_SIZE:
                    return breeding_list
    
    def _mutate_organism_pool(self):
        "Mutates each orginism in the orginism pool"
        for organism in range(self.ORGANISM_POOL_SIZE):
            self.organisms[organism].mutate()
            
    def _set_pool_fitness(self):
        for organism in range(self.ORGANISM_POOL_SIZE):
            self.organisms[organism].set_fitness()
            
    def _order_by_fitness(self):
        "sorts the organisms by fitness"
        self.organisms.sort(lambda x,y: x.fitness - y.fitness)

    def _breed(self, parent_organism1, parent_organism2, child_organism):
        for chromosome in range(self.natural_selector.NUM_CHROMOSOMES):
            random_parent = randint(0, 3)
            if random_parent == 0:
                gene1 = parent_organism1.get_chromosome(chromosome)[0]
                gene2 = parent_organism1.get_chromosome(chromosome)[1]
            elif random_parent == 1:
                gene1 = parent_organism2.get_chromosome(chromosome)[0]
                gene2 = parent_organism2.get_chromosome(chromosome)[1]
            elif random_parent == 2:
                gene1 = parent_organism1.get_chromosome(chromosome)[0]
                gene2 = parent_organism2.get_chromosome(chromosome)[1]
            else:
                gene1 = parent_organism2.get_chromosome(chromosome)[0]
                gene2 = parent_organism1.get_chromosome(chromosome)[1]
                
            child_organism.set_chromosome(chromosome, gene1, gene2)

    def get_organism(self, organism_num):
        "Returns a organism object"
        return self.organisms[organism_num]


def write_wave(file_name, data, channels, sample_rate):
    "Writes the data to a wav file on disk"
    import wave
    wave_output = wave.open( file_name, 'wb' )
    wave_output.setparams( (channels, 2, sample_rate, 0, 'NONE','') )
    wave_output.writeframes( data )
    wave_output.close()

def play_sound(samples):
    import pygame
    import numpy
    convert_to_signed_int(samples)
    pygame.mixer.init()
    sound = pygame.sndarray.make_sound( numpy.array(samples, dtype='int16') )
#    sound.play()
#    import time
#    time.sleep(2)

def get_sampling(file_name):
    "Opens mp3, uncompresses it, and returns the data as well as the channels, and sample rate"
    import pygame
    pygame.mixer.init()
    music = pygame.mixer.Sound(file_name)
    samples = pygame.sndarray.samples(music)
    new_samples = samples.tolist()
    return new_samples[0:10000]

def convert_to_unsigned_int(samples):
    for sample in samples:
        sample[0] += MAX_SAMPLE_INT
        sample[1] += MAX_SAMPLE_INT

def convert_to_signed_int(samples):
    for sample in samples:
        sample[0] -= MAX_SAMPLE_INT
        sample[1] -= MAX_SAMPLE_INT

