from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import folium
from folium import Choropleth, Circle, Marker
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
import matplotlib.colors as colors

    
def facies_plot(logs, facies_colors):
    
    logs = logs.sort_values(by='DEPT')
    cmap_facies = ListedColormap(
            facies_colors)

    ztop=logs.DEPT.min(); zbot=logs.DEPT.max()
    
    cluster=np.repeat(np.expand_dims(logs['Facies_pred'].values,1), 100, 1)
    
    f, ax = plt.subplots(nrows=1, ncols=6, figsize=(19, 16))
    ax[0].plot(logs.GR, logs.DEPT, '-g',linewidth=2)
    ax[1].plot(logs.CALI, logs.DEPT, '-',linewidth=2)
    ax[2].plot(logs.DT, logs.DEPT, '-', color='r',linewidth=2)
    ax[3].plot(logs.Log_ILM, logs.DEPT, '-', color='black',linewidth=2)
    ax[4].plot(logs.Log_ILD, logs.DEPT, '-', color='purple',linewidth=2)
    im=ax[5].imshow(cluster, interpolation='none', aspect='auto',
                    cmap=cmap_facies,vmin=1,vmax=8)
    
    divider = make_axes_locatable(ax[5])
    cax = divider.append_axes("right", size="20%", pad=0.05)
    cbar=plt.colorbar(im, cax=cax)
    cbar.set_label((30*' ').join(['As', 'Aw', 'Ss(F)', 'Ss(A)', 'Ssm',
                 'Sm', 'F(r/a)','F']))
    cbar.set_ticks(range(0,1)); cbar.set_ticklabels('')
    
    
    
    tick_inter = [80,10,0.3,20, 1.1,1.0]
    
    for i in range(len(ax)-1):
        ax[i].set_ylim(ztop,zbot)
        ax[i].invert_yaxis()
        ax[i].grid(which='minor',axis='both')
        ax[i].locator_params(axis='x', nbins=3)
            

    for k in range(8):
                
    
        ax[0].set_xlabel("GR",fontsize=15)
        ax[0].set_xlim(logs.GR.min(),logs.GR.max())
        ax[0].xaxis.set_ticks(np.arange(0, int(logs.GR.max()), tick_inter[0]))
        ax[0].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0i'))
        x = logs.GR

        ax[1].set_xlabel("CALI",fontsize=15)
        ax[1].set_xlim(logs.CALI.min(),logs.CALI.max())
        ax[1].xaxis.set_ticks(np.arange(0, int(logs.CALI.max()), tick_inter[1]))
        ax[1].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0i'))
        x = logs.CALI

    
        ax[2].set_xlabel("DT",fontsize=15)
        ax[2].set_xlim(logs.DT.min(),logs.DT.max())
        ax[2].xaxis.set_ticks(np.arange(logs.DT.min(), int(logs.DT.max()), tick_inter[3]))
        ax[2].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0i'))
        x = logs.DT

        ax[3].set_xlabel("Log_ILM",fontsize=15)
        ax[3].set_xlim(logs.Log_ILM.min(),logs.Log_ILM.max())
        ax[3].xaxis.set_ticks(np.arange(logs.Log_ILM.min(), (logs.Log_ILM.max()), tick_inter[4]))
        ax[3].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        x = logs.Log_ILM
        
        ax[4].set_xlabel("Log_ILD",fontsize=15)
        ax[4].set_xlim(logs.Log_ILD.min(),logs.Log_ILD.max())
        ax[4].xaxis.set_ticks(np.arange(logs.Log_ILD.min(), (logs.Log_ILD.max()), tick_inter[5]))
        ax[4].xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
        x = logs.Log_ILD

        ax[4].set_xlabel('Facies',fontsize=15)

        ax[1].set_yticklabels([]); ax[2].set_yticklabels([]); ax[3].set_yticklabels([])
        ax[4].set_yticklabels([]); ax[5].set_yticklabels([]);
        ax[5].set_xticklabels([])
        
    #f.tight_layout()
    
def facies_plot2(logs, facies_colors):
    #make sure logs are sorted by depth
    logs = logs.sort_values(by='Depth')
    cmap_facies = colors.ListedColormap(
            facies_colors[0:len(facies_colors)], 'indexed')
    
    ztop=logs.Depth.min(); zbot=logs.Depth.max()
    
    cluster=np.repeat(np.expand_dims(logs['Facies'].values,1), 100, 1)
    
    f, ax = plt.subplots(nrows=1, ncols=6, figsize=(8, 12))
    ax[0].plot(logs.GR, logs.Depth, '-g')
    ax[1].plot(logs.ILD_log10, logs.Depth, '-')
    ax[2].plot(logs.DeltaPHI, logs.Depth, '-', color='0.5')
    ax[3].plot(logs.PHIND, logs.Depth, '-', color='r')
    ax[4].plot(logs.PE, logs.Depth, '-', color='black')
    im=ax[5].imshow(cluster, interpolation='none', aspect='auto',
                    cmap=cmap_facies,vmin=1,vmax=9)
    
    divider = make_axes_locatable(ax[5])
    cax = divider.append_axes("right", size="20%", pad=0.05)
    cbar=plt.colorbar(im, cax=cax)
    cbar.set_label((17*' ').join([' SS ', 'CSiS', 'FSiS', 
                                'SiSh', ' MS ', ' WS ', ' D  ', 
                                ' PS ', ' BS ']))
    cbar.set_ticks(range(0,1)); cbar.set_ticklabels('')
    
    for i in range(len(ax)-1):
        ax[i].set_ylim(ztop,zbot)
        ax[i].invert_yaxis()
        ax[i].grid()
        ax[i].locator_params(axis='x', nbins=3)
    
    ax[0].set_xlabel("GR")
    ax[0].set_xlim(logs.GR.min(),logs.GR.max())
    ax[1].set_xlabel("ILD_log10")
    ax[1].set_xlim(logs.ILD_log10.min(),logs.ILD_log10.max())
    ax[2].set_xlabel("DeltaPHI")
    ax[2].set_xlim(logs.DeltaPHI.min(),logs.DeltaPHI.max())
    ax[3].set_xlabel("PHIND")
    ax[3].set_xlim(logs.PHIND.min(),logs.PHIND.max())
    ax[4].set_xlabel("PE")
    ax[4].set_xlim(logs.PE.min(),logs.PE.max())
    ax[5].set_xlabel('Facies')
    
    ax[1].set_yticklabels([]); ax[2].set_yticklabels([]); ax[3].set_yticklabels([])
    ax[4].set_yticklabels([]); ax[5].set_yticklabels([])
    ax[5].set_xticklabels([])
    f.suptitle('Well: %s'%logs.iloc[0]['Well Name'], fontsize=14,y=0.94)
    
    
def compare_facies_plot(logs, compadre, facies_colors):
    #make sure logs are sorted by depth
    logs = logs.sort_values(by='Depth')
    cmap_facies = colors.ListedColormap(
            facies_colors[0:len(facies_colors)], 'indexed')
    
    ztop=logs.Depth.min(); zbot=logs.Depth.max()
    
    cluster1 = np.repeat(np.expand_dims(logs['Facies'].values,1), 100, 1)
    cluster2 = np.repeat(np.expand_dims(logs[compadre].values,1), 100, 1)
    
    f, ax = plt.subplots(nrows=1, ncols=7, figsize=(9, 12))
    ax[0].plot(logs.GR, logs.Depth, '-g')
    ax[1].plot(logs.ILD_log10, logs.Depth, '-')
    ax[2].plot(logs.DeltaPHI, logs.Depth, '-', color='0.5')
    ax[3].plot(logs.PHIND, logs.Depth, '-', color='r')
    ax[4].plot(logs.PE, logs.Depth, '-', color='black')
    im1 = ax[5].imshow(cluster1, interpolation='none', aspect='auto',
                    cmap=cmap_facies,vmin=1,vmax=9)
    im2 = ax[6].imshow(cluster2, interpolation='none', aspect='auto',
                    cmap=cmap_facies,vmin=1,vmax=9)
    
    divider = make_axes_locatable(ax[6])
    cax = divider.append_axes("right", size="20%", pad=0.05)
    cbar=plt.colorbar(im2, cax=cax)
    cbar.set_label((17*' ').join([' SS ', 'CSiS', 'FSiS', 
                                'SiSh', ' MS ', ' WS ', ' D  ', 
                                ' PS ', ' BS ']))
    cbar.set_ticks(range(0,1)); cbar.set_ticklabels('')
    
    for i in range(len(ax)-2):
        ax[i].set_ylim(ztop,zbot)
        ax[i].invert_yaxis()
        ax[i].grid()
        ax[i].locator_params(axis='x', nbins=3)
    
    ax[0].set_xlabel("GR")
    ax[0].set_xlim(logs.GR.min(),logs.GR.max())
    ax[1].set_xlabel("ILD_log10")
    ax[1].set_xlim(logs.ILD_log10.min(),logs.ILD_log10.max())
    ax[2].set_xlabel("DeltaPHI")
    ax[2].set_xlim(logs.DeltaPHI.min(),logs.DeltaPHI.max())
    ax[3].set_xlabel("PHIND")
    ax[3].set_xlim(logs.PHIND.min(),logs.PHIND.max())
    ax[4].set_xlabel("PE")
    ax[4].set_xlim(logs.PE.min(),logs.PE.max())
    ax[5].set_xlabel('Facies')
    ax[6].set_xlabel(compadre)
    
    ax[1].set_yticklabels([]); ax[2].set_yticklabels([]); ax[3].set_yticklabels([])
    ax[4].set_yticklabels([]); ax[5].set_yticklabels([])
    ax[5].set_xticklabels([])
    ax[6].set_xticklabels([])
    f.suptitle('Well: %s'%logs.iloc[0]['Well Name'], fontsize=14,y=0.94)
