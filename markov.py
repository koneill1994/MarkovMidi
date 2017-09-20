# implementation of an nth-order markov chain model
# to learn and simulate midi music
# but could be used to generalize to any kind of data

# Kevin O'Neill

import random, string, pickle



# adapted from moooeeeep, stackoverflow
def weighted_choice(choices, total):
   r = random.uniform(0, total)
   upto = 0
   for c in choices:
      if upto + choices[c] >= r:
         return c
      upto += choices[c]
   assert False, "Shouldn't get here"

class Markov:
  # etc
  def __init__(self):
    self.states = {} #name of item, object of item
  
  def find_state(self, c):
    if c not in self.states.keys():
      self.states[c] = MarkovState(c)
    return self.states[c]
  
  def add_data(self, data):
    last=None
    for item in data:
      tmp=self.find_state(item)
      if last!=None:
        last.add_datum(tmp)
      last=tmp
  
  def print_states(self):
    for obj in self.states.values():
      print obj.content
      for n in obj.next_state:
        print "  " + n.content
        print "    " + str(1.0*obj.next_state[n]/obj.next_state_sum)


class MarkovState:
  
  def __init__(self, c):
    self.content = c
    self.next_state ={}
    self.next_state_sum=0
    
  def add_datum(self, datum):
    if datum not in self.next_state.keys():
      self.next_state[datum]=0
    self.next_state[datum]+=1
    self.next_state_sum+=1
    
  def get_next_state(self):
    return weighted_choice(self.next_state, self.next_state_sum)
    
    
# testing #


#'''
test = "Let this be the hour when we draw swords together. Fell deeds awake. Now for wrath, now for ruin, and the red dawn".translate(None, string.punctuation).split()

m=Markov()
m.add_data(test)

f = open('lincoln_corpus.txt','r')
c=0
for line in f:
  if c%10 == 0:
    print "reading line " + str(c) + " of lincoln_corpus.txt"
  m.add_data(line.translate(None, string.punctuation).split())
  c+=1

f.close()

bible = open('bible_corpus.txt','r')
c=0
for line in bible:
  if c%10 == 0:
    print "reading line " + str(c) + " of bible_corpus.txt"
  m.add_data(line.translate(None, string.punctuation).split())
  c+=1

bible.close()
#'''


pickle.dump( m, open( "markov_dump.p", "wb" ) )


m = pickle.load( open( "markov_dump.p", "rb" ) )


m.print_states()


