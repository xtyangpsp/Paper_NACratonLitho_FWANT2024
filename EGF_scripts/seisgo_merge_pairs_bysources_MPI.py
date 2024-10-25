import sys,time,os, glob
from multiprocessing import Pool
from seisgo import noise,utils
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

'''
Stacking script of SeisGo to:
    1) load cross-correlation data for each station pair
    2) merge all time chuncks
    3) save outputs in ASDF;
'''
########################################
#########PARAMETER SECTION##############
########################################
#get arguments on the number of processors

# absolute path parameters
def merge_wrapper(ccfiles,pair,outdir):
    to_egf = True                                               #convert CCF to empirical Green's functions when merging
    stack = True
    stack_method = "robust"
    stack_win_len = 30*24*3600
    flag   = True 
    noise.merge_pairs(ccfiles,pair,outdir=outdir,verbose=flag,to_egf=to_egf,stack=stack,
                        stack_method=stack_method,stack_win_len=stack_win_len)
    return 0

def main():
    narg=len(sys.argv)
    if narg == 1:
        nproc=1
    else:
        nproc=int(sys.argv[1]) 

    ## Global parameters
    rootpath  = "data_craton"                                 # root path for this data processing
    CCFDIR    = os.path.join(rootpath,'CCF_SOURCES')                            # dir where CC data is stored
    MERGEDIR  = os.path.join(rootpath,'MERGED_PAIRS')                          # dir where stacked data is going to
    if not os.path.isdir(MERGEDIR):os.makedirs(MERGEDIR)
    #######################################
    ###########PROCESSING SECTION##########
    #######################################

    #loop through resources, for each source MPI through station pairs.
    sources_temp=utils.get_filelist(CCFDIR)
    #exclude non-directory item in the list
    sources=[]
    for src in sources_temp:
        if os.path.isdir(src): sources.append(src)

    for src in sources:
        tt0=time.time()

        # cross-correlation files
        ccfiles = utils.get_filelist(src,"h5")
        print("assembled %d files"%(len(ccfiles)))
        pairs_all,netsta_all=noise.get_stationpairs(ccfiles,False)
        print("found %d station pairs for %d stations"%(len(pairs_all),len(netsta_all)))

        #loop for each station pair
        print("working on all pairs with %d processors."%(nproc))
        if nproc < 2:
            results=merge_wrapper(ccfiles,pairs_all,MERGEDIR)
        else: 
            p=Pool(int(nproc))
            results=p.starmap(merge_wrapper,[(ccfiles,pair,MERGEDIR) for pair in pairs_all])
            p.close()
        del results


        print('it takes %6.2fs to merge %s' % (time.time()-tt0,src))
        # 
if __name__ == "__main__":
    main()
