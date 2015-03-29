import liblo
import time
import numpy
import math
import winsound
import time
from random import random, randint

class MusicIndividual(): #Container for parameters and basic functions
    def __init__ (self):        
        self.c1 = 0
        self.c2 = 0
        self.alpha = 0
        self.beta = 0
        self.time = time.time()
        
    def evaluate(self, timer):
        ''' Returns tone value from 0-127'''
        self.timer = timer
        return self.c1*math.sin(self.alpha*timer) + self.c2*math.cos(self.beta*timer) + self.c1 + self.c2 + 37
        
    def randomize(self):
        ''' Required for Evolvable subclass '''
        self.c1 = randint(37,2500)
        self.c2 = randint(37,2500)
        self.alpha = random()
        self.beta = random()
        
        
    def mutate(self):
        ''' Required for Evolvable subclass 
            an operator that does a small step in search space, 
            according to some distance metric. The genes of chromosome are 
            altered based by applying mutation rate (by random generator) 
            to each gene.'''
            
        mutationrate = 0.5
        self.c1 += max(0, (min(self.c1 - random()*mutationrate, 10)))
        self.c2 += max(0, (min(self.c2 - random()*mutationrate, 10)))
        self.alpha += max(0, (min(self.alpha - random()*mutationrate, 10)))
        self.beta += max(0, (min(self.beta - random()*mutationrate, 10)))
        
    def param_list(self):
        return [self.c1,
                self.c2,
                self.alpha,
                self.beta]
    
def create(indiv, variance, timer):
    for i in range(variance % 500):
        indiv.mutate()
    winsound.Beep(int(indiv.evaluate(timer)), 200)
    time.sleep(random()/10)

class CircBuff():
    def __init__(self, len):
        self.data = numpy.zeros(len,dtype='f')
        self.index = 0
        self.len = len
        
    def add(self, x):
        if self.index >= self.len:
            self.index = 0
        self.data[self.index] = x
        self.index += 1
        
    def var(self):
        return numpy.var(self.data)

museServer = liblo.Server(5000, liblo.TCP)
buffs = [CircBuff(100) for buffer in range(4)]

def eeg_callback(path, args):
    [buff.add(f) for buff in buffs for f in args]
    f1,f2,f3,f4 = args
    print("'%s' with args '%f', '%f', '%f', '%f'" % (path, f1, f2, f3, f4))
    
museServer.add_method("/muse/eeg", 'ffff', eeg_callback, buffs)
i = 0
indiv = MusicIndividual()
indiv.randomize()
while True:    
    i += 1
    print(int(buffs[0].var()))
    create(indiv, int(buffs[0].var()), i)
    time.sleep(.05)
    museServer.recv(100)
