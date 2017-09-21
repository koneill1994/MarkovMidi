# implementation of an nth-order markov chain model
# to learn and simulate midi music
# but could be used to generalize to any kind of data

# Kevin O'Neill

import random, string, pickle, sys
import Queue


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
  
  def __init__(self):
    self.states = {} #name of item, object of item
    self.markov_order=2
  
  def find_state(self, c):
    if c not in self.states.keys():
      self.states[c] = MarkovState(c)
    return self.states[c]
  
  def add_data(self, data):
    last=None
    self.q=[]
    for item in data:
      self.q.append(item)
      if len(self.q)>self.markov_order:
        self.q=self.q[1:]
      if last!=None:
        last.add_datum(item)
      last=self.find_state(tuple(self.q))
  
  def print_states(self):
    num_c = 0
    num_w=0
    for obj in self.states.values():
      num_w+=1
      print obj.content
      for n in obj.next_state:
        print "  " + str(n)
        print "    " + str(1.0*obj.next_state[n]/obj.next_state_sum)
        num_c+=1
    print "DATABASE:"
    print str(num_w) + " WORDS"
    print str(num_c) + " CONNECTIONS"

  def generate_text(self):
    node = self.states[random.choice(self.states.keys())]
    text=' '.join(node.content)
    q=list(node.content)
    for x in range(0,100):
      q[1:].append(node.get_next_state())
      new_node = self.find_state(tuple(q))
      text+=" "+new_node.content[-1]
      node=new_node
    print text

# some work needs to be done here to implement nth-order
class MarkovState:
  
  def __init__(self, c):
    self.content = c
    self.next_state = {}
    self.next_state_sum=0
    
  def add_datum(self, datum):
    if datum not in self.next_state.keys():
      self.next_state[datum]=0
    self.next_state[datum]+=1
    self.next_state_sum+=1
    
  def get_next_state(self):
    if self.next_state_sum <= 1:
      return "_"
    return weighted_choice(self.next_state, self.next_state_sum)
    
    
loadOnly=False
    
    
# testing #
linelimit=None

if(not loadOnly):
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
  
  linelimit=250
  
  bible = open('bible_corpus.txt','r')
  c=0
  for line in bible:
    if c%10 == 0:
      print "reading line " + str(c) + " of bible_corpus.txt"
    m.add_data(line.translate(None, string.punctuation).split())
    c+=1
    if linelimit!= None and c>linelimit:
      break
  
  bible.close()
  #'''
  
  
  pickle.dump( m, open( "markov_dump.p", "wb" ) )

else:
  m = pickle.load( open( "markov_dump.p", "rb" ) )


m.print_states()

m.generate_text()
