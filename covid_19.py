# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 11:21:04 2020

@author: Benedict
"""

import random
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

fig, (ax1, ax2) = plt.subplots(1, 2)

class Disease:
    def __init__(self,infection_probability,infection_radius,infection_dubriation,mortality_rate):
        self.infection_probability=infection_probability
        self.infection_dubriation=infection_dubriation
        self.infection_radius=infection_radius

class Patient:
    def __init__(self,infection,status='sus',social_disatance=False):
        self.pos=[random.random()*10,random.random()*10]
        self.infection=infection
        self.status=status
        self.vel=[0,0]
        self.acc=[0,0]
        self.deltaT=0.25
        self.infection_counter=0
        self.social_disatance=social_disatance
        self.market=False
        self.market_counter=0
        
    def compute_distance(self,other_person):
        x=pow(self.pos[0]-other_person.pos[1],2) + pow(self.pos[1]-other_person.pos[1],2)
        return(x**0.5)
    
    def rd_move(self,others=None):
        self.acc[0]=(1-2*random.random())*0.01/self.deltaT
        self.acc[1]=(1-2*random.random())*0.01/self.deltaT
        
        if self.social_disatance and type(others)!=type(None):
            tmp_a=[0,0]
            for i in others:
                if self.compute_distance(i)!=0 and self.compute_distance(i)<=self.infection.infection_radius:
                    tmp_a[0]=tmp_a[0]-(self.pos[0]-i.pos[0])/self.compute_distance(i)*0.25
                    tmp_a[1]=tmp_a[1]-(self.pos[1]-i.pos[1])/self.compute_distance(i)*0.25
            if tmp_a[0]!=0 and tmp_a[1]!=0:
                self.acc[0]=tmp_a[0]
                self.acc[1]=tmp_a[1]

        self.vel[0]=self.vel[0]+self.acc[0]*self.deltaT
        self.vel[1]=self.vel[1]+self.acc[1]*self.deltaT        
        
        
        v=pow(self.vel[0]**2+self.vel[1]**2,0.5)
        if v>0.3:
            self.vel[0]=self.vel[0]/v*0.3
            self.vel[1]=self.vel[1]/v*0.3
            
        if self.market:
            self.go_to_market()

        self.pos[0]= self.pos[0]+self.vel[0]*self.deltaT +0.5*self.acc[0]*self.deltaT**2 
        self.pos[1]= self.pos[1]+self.vel[1]*self.deltaT +0.5*self.acc[1]*self.deltaT**2 
    
    
    
    def infect_others(self,others):
        if self.status=='inf':
            for i in others:
                if i.status=='sus':
                    if self.compute_distance(i)<=self.infection.infection_radius and self.compute_distance(i)!=0:
                        if random.random()<=self.infection.infection_probability*self.deltaT:
                            i.status='inf'

    
    def recover(self):
        if self.status=='inf':
            self.infection_counter=self.infection_counter+1
        if self.infection_counter>= self.infection.infection_dubriation/self.deltaT:
            self.status='rm'


    def go_to_market(self):
        if self.market:
            if self.market_counter==0:
                self.save_pos=self.pos
                self.vel[0]=5-self.pos[0]
                self.vel[1]=5-self.pos[1]
            if self.market_counter/self.deltaT==1:
                self.vel=[0,0]
            if self.market_counter/self.deltaT>=2:
                self.vel[0]=-(5-self.save_pos[0])
                self.vel[1]=-(5-self.save_pos[1])                
            if self.market_counter/self.deltaT>3:
                self.market=False
                self.market_counter=0
                self.vel=[0,0]

            else:
                self.market_counter=self.market_counter+1
                
                
class Test_field:
    def __init__(self,sample_size,disease,social_distance=0):
        self.Disease=Disease
        self.Patients=list()

        ### geneartes the population        
        for i in range(sample_size):
            if random.random() <= 0.1:
                self.Patients.append(Patient(disease,status='inf'))
            else:
                self.Patients.append(Patient(disease))
        
        ###activate social distance for a part of the population
        for i in self.Patients:
            if random.random() <=social_distance:
                i.social_disatance=True
        
        
        ### boundary for the simulation
        self.upper_boundary=10
        self.lower_boundary=0
        ### lists for plotting the graphs
        self.inf_plot=list()
        self.sus_plot=list()
        self.rm_plot=list()

    def max_vel(self,others):
        maxvel=max([pow(i.vel[0]**2+i.vel[1]**2,0.5) for i in others])
        print(maxvel)
        
    def average_distance(self):
        average_dist=list()
        for i in self.Patients:
            average_dist.append(min([i.compute_distance(k) for k in self.Patients if i.compute_distance(k)>0]))
        print(sum(average_dist)/len(average_dist))

    def number_in_infection_range(self):
        average_dist=list()
        for i in self.Patients:
            if i.infection.infection_radius >= min([i.compute_distance(k) for k in self.Patients if i.compute_distance(k)>0]):
                average_dist.append(1)
        print(len(average_dist))

        
    def boundary_condition(self,i):
        if i.pos[0]> self.upper_boundary:
            i.vel[0]=-0.025
            i.pos[0]= self.upper_boundary
        if i.pos[1]> self.upper_boundary:
            i.vel[1]=-0.025
            i.pos[1]= self.upper_boundary
        if i.pos[0]< self.lower_boundary:
            i.vel[0]=0.025    
            i.pos[0]= self.lower_boundary
        if i.pos[1]< self.lower_boundary:
            i.vel[1]=0.025
            i.pos[1]= self.lower_boundary


    def simulate(self,plot='False'):
        inf=list()
        sus=list()
        rm=list()
        for i in range(int(100/self.Patients[0].deltaT)):
            for i in self.Patients:
                i.rd_move()
                i.infect_others(self.Patients)
                i.recover()
                self.boundary_condition(i)
            if plot:
                tmp_inf=0
                tmp_sus=0
                tmp_rm=0
                for i in self.Patients:
                    if i.status=='sus':
                        tmp_sus=tmp_sus+1
                    
                    if i.status=='inf':
                        tmp_inf=tmp_inf+1
                        
                    if i.status=='rm':
                        tmp_rm=tmp_rm+1
                sus.append(tmp_sus)
                inf.append(tmp_inf)
                rm.append(tmp_rm)
            plt.plot(sus)
            plt.plot(inf)
            plt.plot(rm)
            
            
    def simulate_timestep(self):
        for i in self.Patients:
            if random.random()<=0.0:
                i.market=True
            i.rd_move(others=self.Patients)
            i.infect_others(self.Patients)
            i.recover()
            self.boundary_condition(i)

    def realtime_plot_update(self,i):
        ax1.clear()
        self.simulate_timestep()
        sus=[[x.pos[0],x.pos[1]] for x in self.Patients if x.status=='sus']
        inf=[[x.pos[0],x.pos[1]] for x in self.Patients if x.status=='inf']        
        rm=[[x.pos[0],x.pos[1]] for x in self.Patients if x.status=='rm']
        
        sus=np.array(sus)
        inf=np.array(inf)
        rm=np.array(rm)
        
        #scatter plot
        ax1.set_xlim([0,10])
        ax1.set_ylim([0,10])
        ax1.scatter(sus[:,0],sus[:,1],c=('green'))
        if len(inf)>0:
            ax1.scatter(inf[:,0],inf[:,1],c=('red'))
        if len(rm)>0:
            ax1.scatter(rm[:,0],rm[:,1],c=('grey'))
        
        #graph plot
        self.sus_plot.append(len(sus))
        self.inf_plot.append(len(inf))
        self.rm_plot.append(len(rm))
        
        ax2.plot(self.sus_plot,color='g',label='Susceptible')
        ax2.plot(self.inf_plot,color='r',label='Infected')
        ax2.plot(self.rm_plot,color='grey',label='Removed')
        ax2.legend(labels=['Susceptible','Infected','Removed'])
        
#        for k in self.Patients:
#            print(k.market)
        
        if i%20==0:
            self.get_result()
            #self.max_vel(self.Patients)
            #self.average_distance()
            #self.number_in_infection_range()


    def realtime_plot_graph(self,i):
        self.simulate_timestep()
        tmp_inf=0
        tmp_sus=0
        tmp_rm=0
        for i in self.Patients:
            if i.status=='sus':
                tmp_sus=tmp_sus+1
            
            if i.status=='inf':
                tmp_inf=tmp_inf+1
                
            if i.status=='rm':
                tmp_rm=tmp_rm+1
        self.sus_plot.append(tmp_sus)
        self.inf_plot.append(tmp_inf)
        self.rm_plot.append(tmp_rm)
        plt.plot(self.sus_plot,color='g',label='Susceptible')
        plt.plot(self.inf_plot,color='r',label='Infected')
        plt.plot(self.rm_plot,color='grey',label='Removed')
        plt.legend(labels=['sus','inf','rm'])

    def get_result(self):
        sus=[x for x in self.Patients if x.status=='sus']
        inf=[x for x in self.Patients if x.status=='inf']        
        rm=[x for x in self.Patients if x.status=='rm']
        mk=[x for x in self.Patients if x.market]
        print('Result:')
        print('Susceptible: '+str(len(sus)))
        print('Infected: '+str(len(inf)))
        print('Removed: '+str(len(rm)))
        print('Market: '+str(len(mk)))


if __name__=='__main__':
    covid_19=Disease(0.2,0.2,50,0)
    
    t0=Test_field(300,covid_19)
    ani = animation.FuncAnimation(fig, t0.realtime_plot_update)
