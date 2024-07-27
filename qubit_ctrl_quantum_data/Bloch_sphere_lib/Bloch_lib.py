import matplotlib as mpl
mpl.use('MacOSX')

from qutip_bloch import *
import numpy as np


from pylab import *
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

import os, sys

#read in local directory path
str1=os.getcwd()
str2=str1.split('\\')
n=len(str2)
my_dir = str2[n-1]


def Bloch_plots(states, times, target, file_name='test', movie_frames=False):

	# preallocate variables
	Fidelity=[]
	# create Bloch class object
	points=[]
	i=0
	for i, psi in enumerate(states):
		# instantaneous fidelity
		Fidelity.append( abs(psi.conj().dot(target))**2 )
		
		# Bloch sphere image
		bloch = Bloch()

		# add instantaneous fidelity
		ann_pos = np.array([-0.22,-.68,1.02])
		#ann_pos/=np.linalg.norm(ann_pos)
		ann_str="$F(t{=}"+"{0:.2f})".format(times[i])+"{=}"+"{0:.3f}$".format(np.around(Fidelity[i],3) )
		bloch.add_annotation(ann_pos, ann_str, fontsize=18)
		
		# plot the states as arrow
		bloch.add_states([psi,target], colors=[['b'],['r']] )
		# extract spherical coordinates of psi
		points.append(bloch.vectors[0])
		# plot all psi's as blue dots
		bloch.point_color = ['b']
		bloch.add_points([list(a) for a in zip(*points)], meth='l')
		# plot psi_target
		bloch.add_points(bloch.vectors[1])
		
		# set view angle
		bloch.view = [40,10]
		bloch.set_label_convention("xy")
		bloch.show()


		#store data
		save_dir=my_dir+"/bloch_plots/"
		if not os.path.exists(save_dir):
		    os.makedirs(save_dir)
		bloch.save(name=save_dir+file_name+'_{}.pdf'.format(i),)

		if movie_frames:
			save_dir=my_dir+"/movie_frames/"
			if not os.path.exists(save_dir):
			    os.makedirs(save_dir)
			bloch.save(name=save_dir+file_name+'_{}.png'.format(i), dpi=300)

		
		bloch.clear()
		plt.close()

	return Fidelity

	

def Bloch_movie(states, times, target, movie_name='test'):
			

	Fidelity = Bloch_plots(states, times, target, file_name='frame', movie_frames=True)

	# create movie
	frame_dir = my_dir + '/movie_frames'
	cmd = "ffmpeg -framerate 5 -i " + frame_dir+"/frame_%01d.png -c:v libx264 -r 30 -pix_fmt yuv420p " + 'bloch_plots/'+movie_name+".mp4"
	print(cmd)
	# execute command cmd
	os.system(cmd)
	# remove temp directory
	os.system("rm -rf movie_frames*")
	
	return Fidelity
