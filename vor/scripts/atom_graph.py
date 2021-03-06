from pprint import pprint
import os
import time
import random
import string
from vor import Vor
import categorize_vor
from hutch import Hutch
from model import Model
import voronoi_3d
import sys
import numpy as np

class AtomGraph(object):
    """ Implements a graph made up of atoms from a model.
        A cutoff is necessary to determine atom neighbors. """

    def __init__(self,modelfile,cutoff):
        """ Constructor
        @param cutoff is the cutoff we will use to determine neighbors """

        super(AtomGraph,self).__init__()
        
        self.model = Model(modelfile)
        #self.model.generate_neighbors(cutoff)
        #self.model.generate_coord_numbers()
        #print('Coordination numbers:')
        #pprint(self.model.coord_numbers)
        #self.model.print_bond_stats()

        # Generate CNs for different cutoffs. I can plot this and find
        # where it changes the least (ie deriv=0); this is a good spot
        # to set the cutoff distances because then the neighbors are
        # the least dependent on the cutoff distance.
        # I should make this into a function in model.py TODO
        #for cut in np.arange(2.0,4.6,0.1):
        #    self.model.generate_neighbors(cut)
        #    self.model.generate_coord_numbers()
        #    print("Cutoff: {0}".format(cut))
        #    for key in self.model.coord_numbers:
        #        if(len(key) < 4):
        #            print('  {0}: {1}'.format(key,self.model.coord_numbers[key]))

        #vor_instance = Vor()
        #vor_instance.runall(modelfile,cutoff)
        #index = vor_instance.get_index()
        #
        #vorcats = VorCats('/home/jjmaldonis/OdieCode/vor/scripts/categorize_parameters.txt')
        #vorcats.save(index)
        #vorcats.save_vps(self.model)
        #
        #self.vp_dict = vorcats.get_vp_dict()

        #self.atom_dict = vorcats.get_atom_dict()
        ##for key in self.atom_dict:
        ##    print("{0} {1}".format(key,self.atom_dict[key]))
        #for key in self.atom_dict:
        #    for i in range(0,len(self.atom_dict[key])):
        #        self.atom_dict[key][i] = self.atom_dict[key][i][0]
        ##for key in self.atom_dict:
        ##    print("{0} {1}".format(key,len(self.atom_dict[key])))
        ##    #print("{0} {1}".format(key,self.atom_dict[key]))

        ##self.values = {}
        ##for atom in self.model.atoms:
        ##    for key in self.atom_dict:
        ##        if atom.id in self.atom_dict[key]:
        ##            self.values[atom] = key[:-1]
        ##    if atom not in self.values:
        ##        print("CAREFUL! SOMETHING WENT WRONG!")
        ##        #self.values[atom] = "Undef"
        ##for key in self.values:
        ##    print("{0}: {1}".format(key,self.values[key]))

        # Let's also run our VP algorithm to generate all that info.
        #voronoi_3d.voronoi_3d(self.model,cutoff)


    def get_common_neighs(self,atom,*types):
        neighs = self.get_neighs(atom)
        list = [ atom for atom in neighs if atom.compute_vp_type(self.model.vp_dict) in types ]
        #list = [ atom for atom in neighs if atom.vp.type in types ]
        #list = []
        #for atom in neighs:
        #    if atom.get_vp_type(self.model.vp_dict) in types:
        #        list.append(atom)
        return list

    def get_unvisited_common_neighs(self,atom,visited,*types):
        comm_neighs = self.get_common_neighs(atom,*types)
        for atom in visited:
            if visited[atom] and atom in comm_neighs:
                comm_neighs.remove(atom)
        return comm_neighs

    def get_clusters(self,*cluster_types):
        connections = {}
        #print("Connections:")
        for atom in self.model.atoms:
            connections[atom] = self.get_common_neighs(atom,*cluster_types)
            #print("Atom {0}: {1}".format(atom,connections[atom]))

        clusters = []

        # Find an atom of type cluster_types
        atoms = self.model.atoms
        temp_atoms = [x for ctype in cluster_types for x in self.atom_dict[ctype+':'] ]
        for atom in temp_atoms:
            start_atom = atoms[atom] # atom represents the id in for this format - it's an int! not an atom
        
            visited = {start_atom:True}

            neighs = self.get_unvisited_common_neighs(start_atom,visited,cluster_types)
            # neighs now contains all the neighbors of start_atom that have the same vp type as it
            # and that we have not visited already.

            paths = [] # this will contain all possible paths we find!
            path = [start_atom] # this will contain our current path
            queue = connections[start_atom]
            here = False
            prepop = -1
            while(len(path)):
                for atom in visited:
                    if atom in queue and visited[atom]:
                        queue.remove(atom)
                if(len(queue)):
                    path.append(queue[0])
                    visited[queue[0]] = True
                    queue = connections[queue[0]]
                    here = True
                else:
                    if(here):
                        #print(path)
                        paths.append(path[:])
                    #else:
                    #    print("Not including: {0}".format(path))
                    here = False
                    if(type(prepop) != type(-1)):
                        visited[prepop] = False
                    #
                    prepop = path.pop()
                    if not len(path):
                        break
                    queue = connections[path[-1]]
            cluster = [ atom  for pathi in paths for atom in pathi ]
            cluster = list(set(cluster)) # remove duplicates
            cluster.sort()
            if cluster != [] and cluster not in clusters:
                clusters.append(cluster)
        return clusters
 


def main():
    cluster_type = 'Crystal-like'
    #cluster_type = 'Icosahedra-like'

    ag = AtomGraph(sys.argv[1],3.5)
   
    #clusters = ag.get_clusters(cluster_type)
    #i = 1
    #for cluster in clusters:
    #    print("Unique cluster {0}: {1} atoms".format(i,len(cluster)))
    #    i += 1
    #    for atom in cluster:
    #        print(atom.vesta())

    #print(ag.model.atoms[0].get_vp_type(ag.model.vp_dict))


if __name__ == "__main__":
    main()
        
