"""Create a static design preview from the same source used by Tableau.

This is a layout preview, NOT a screenshot exported from Tableau.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.ticker import FuncFormatter

ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/credit_card_portfolio_2025.csv',parse_dates=['Snapshot_Month'])
NAVY='#142D44'; TEAL='#187F7A'; BLUE='#287C96'; AMBER='#C58043'; GRAY='#647889'; BG='#F5F8FB'
plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False,'axes.edgecolor':'#DDE5EB','xtick.color':GRAY,'ytick.color':GRAY,'axes.labelcolor':GRAY,'font.size':11,'axes.titleweight':'bold','axes.titlecolor':NAVY})
fig=plt.figure(figsize=(16,10.6),facecolor=BG)
fig.text(.052,.951,'CREDIT CARD PORTFOLIO',size=25,weight='bold',color=NAVY)
fig.text(.054,.921,'Revenue and risk review   |   2025 monthly account snapshots   |   Synthetic data',size=11,color=GRAY)

cards=[('TRANSACTION VOLUME','$46.0M',TEAL),('INTEREST INCOME','$8.0M',BLUE),('DELINQUENCY RATE','6.0%',AMBER),('ACTIVE ACCOUNTS','3,000',NAVY)]
for i,(label,value,c) in enumerate(cards):
    x=.052+i*.235
    fig.add_artist(FancyBboxPatch((x,.777),.22,.117,boxstyle='round,pad=0.006,rounding_size=.013',transform=fig.transFigure,facecolor='white',edgecolor='#E5ECF0',linewidth=.9,zorder=-1))
    fig.text(x+.016,.855,label,color=GRAY,size=10,weight='bold')
    fig.text(x+.016,.805,value,color=c,size=24,weight='bold')

# plotting cards using axes positions
month=df.groupby('Snapshot_Month').agg(spend=('Transaction_Volume_USD','sum'),delinq=('Delinquent_Flag','mean'))

def panel(rect,title):
    x,y,w,h=rect
    fig.add_artist(FancyBboxPatch((x-.005,y-.016),w+.01,h+.049,boxstyle='round,pad=.007,rounding_size=.01',transform=fig.transFigure,facecolor='white',edgecolor='#E5ECF0',linewidth=.8,zorder=-1))
    ax=fig.add_axes((x+.025,y+.035,w-.05,h-.06))
    fig.text(x+.018,y+h+.004,title,size=12,weight='bold',color=NAVY)
    return ax

ax=panel((.052,.427,.455,.286),'Monthly transaction volume')
ax.plot(month.index,month.spend/1e6,marker='o',color=TEAL,linewidth=2.5,markersize=4.5)
ax.set_ylim(0,6)
ax.set_ylabel('$ millions',fontsize=9)
ax.set_xticks(month.index[::2]);ax.set_xticklabels([t.strftime('%b') for t in month.index[::2]])
ax.grid(axis='y',alpha=.16)
ax=panel((.537,.427,.411,.286),'Delinquency trend')
ax.plot(month.index,100*month.delinq,color=AMBER,marker='o',linewidth=2.5,markersize=4.5)
ax.set_ylabel('% account-months',fontsize=9)
ax.set_ylim(4,8)
ax.set_xticks(month.index[::2]);ax.set_xticklabels([t.strftime('%b') for t in month.index[::2]])
ax.grid(axis='y',alpha=.16)

by_tier=(df.groupby('Card_Tier')['Transaction_Volume_USD'].sum()/1e6).sort_values()
ax=panel((.052,.092,.287,.264),'Spend by card tier')
ax.barh(by_tier.index,by_tier.values,color=TEAL,alpha=.9,height=.56)
for j,v in enumerate(by_tier.values):ax.text(v+.22,j,f'${v:.1f}M',color=NAVY,va='center',size=10)
ax.set_xlim(0,21.5);ax.set_xticks([0,10,20]);ax.set_xlabel('$ millions',fontsize=9)
ax=panel((.369,.092,.277,.264),'Delinquency by risk segment')
by_risk=(df.groupby('Risk_Segment')['Delinquent_Flag'].mean()*100).sort_values()
ax.barh(by_risk.index,by_risk.values,color=AMBER,alpha=.9,height=.58)
for j,v in enumerate(by_risk.values):ax.text(v+.55,j,f'{v:.1f}%',color=NAVY,va='center',size=9)
ax.set_xlim(0,42);ax.set_xticks([0,20,40]);ax.set_xlabel('Delinquent %',fontsize=9)
ax=panel((.676,.092,.272,.264),'Interest by region')
by_reg=(df.groupby('Region')['Interest_Income_USD'].sum()/1e6).sort_values()
ax.barh(by_reg.index,by_reg.values,color=BLUE,alpha=.9,height=.53)
for j,v in enumerate(by_reg.values):ax.text(v+.035,j,f'${v:.2f}M',color=NAVY,va='center',size=9)
ax.set_xlim(0,3.1);ax.set_xticks([0,1,2,3]);ax.set_xlabel('$ millions',fontsize=9)
fig.text(.054,.025,'Prepared for Suhas Ramachandra  •  This is a static design preview, not a Tableau screenshot.',size=9,color=GRAY)
p=ROOT/'docs'/'design-preview.png'
fig.savefig(p,dpi=140,facecolor=BG)
print(p)
