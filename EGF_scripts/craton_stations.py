import sys,time,os, glob
from mpi4py import MPI
from seisgo import noise
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

tt0=time.time()
########################################
#########PARAMETER SECTION##############
########################################
# absolute path parameters
rootpath  = "/Users/xtyang/Work/Research/Projects/Craton/data/data_craton"                                 # root path for this data processing
CCFDIR    = os.path.join(rootpath,'CCF_me')                            # dir where CC data is stored
os.listdir(CCFDIR)
ccfiles   =  sorted([os.path.join(CCFDIR,f) for f in os.listdir(CCFDIR) if f[-2:].lower()=="h5"])
print("assembled %d files"%(len(ccfiles)))
pairs_all,netsta_all=noise.get_stationpairs(ccfiles,False)
npairs  = len(pairs_all)
nsta=len(netsta_all)
print("found %d station pairs for %d stations"%(npairs,nsta))
    
