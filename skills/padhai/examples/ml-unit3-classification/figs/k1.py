import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))  # padhai/scripts
from fig_lib import *
rng=np.random.default_rng(3)
def sc(ax): ax.set_xticks([]); ax.set_yticks([])

# --- binary vs multiclass ---
f,axs=plt.subplots(1,2,figsize=(7.2,2.9))
ax=axs[0]; a=rng.normal([2,2],0.6,(25,2)); b=rng.normal([4.5,4.2],0.6,(25,2))
ax.scatter(*a.T,c=C[0],s=22,marker='o',label='Class 0 (Not spam)'); ax.scatter(*b.T,c=C[1],s=26,marker='^',label='Class 1 (Spam)')
xx=np.linspace(0.3,6.3,10); ax.plot(xx,6.4-xx,'k--',lw=1.2)
ax.set_title('(a) Binary: 2 classes, 1 boundary',fontsize=9.5); ax.legend(fontsize=7.4,loc='upper left',frameon=False); ax.set_xlim(0,6.6); ax.set_ylim(0,7.2); sc(ax)
ax=axs[1]; cs=[([2,2],'o','Cat'),([5,2.2],'^','Dog'),([3.5,5],'s','Rabbit')]
for i,(m,mk,l) in enumerate(cs):
    p=rng.normal(m,0.55,(18,2)); ax.scatter(*p.T,c=C[i],s=22,marker=mk,label=l)
ax.plot([3.5,3.5],[0,3.4],'k--',lw=1.2); ax.plot([3.5,0.3],[3.4,4.6],'k--',lw=1.2); ax.plot([3.5,6.8],[3.4,4.6],'k--',lw=1.2)
ax.set_title('(b) Multiclass: 3 classes, several boundaries',fontsize=9.5); ax.legend(fontsize=7.4,loc='upper left',frameon=False,ncol=3); ax.set_xlim(0,7); ax.set_ylim(0,7.2); sc(ax)
f.tight_layout(); save(f,'types')

# --- balanced vs imbalanced ---
f,axs=plt.subplots(1,2,figsize=(6.8,2.4))
for ax,v,t in [(axs[0],[500,500],'(a) Balanced (50 : 50)'),(axs[1],[990,10],'(b) Imbalanced (99 : 1)')]:
    bars=ax.bar(['Negative','Positive'],v,color=[C[0],C[4]],width=0.55)
    for bb,val in zip(bars,v): ax.text(bb.get_x()+bb.get_width()/2,val+20,str(val),ha='center',fontsize=9)
    ax.set_ylim(0,1120); ax.set_title(t,fontsize=9.5); ax.set_ylabel('No. of samples',fontsize=8.5)
f.tight_layout(); save(f,'imb')

# --- linear classifier ---
f,ax=plt.subplots(figsize=(4.4,3.3))
P=np.array([[4,3],[3.5,2.5],[4.5,1.5],[3,3.5],[5,2.2]]); N=np.array([[1,1],[0.5,2],[1.5,0.5],[1,3],[2,0.8]])
ax.scatter(*P.T,c=C[1],marker='^',s=40,label='Class +1  (w·x + b > 0)'); ax.scatter(*N.T,c=C[0],s=36,label='Class −1  (w·x + b < 0)')
xx=np.linspace(1.0,3.6,10); ax.plot(xx,6-2*xx,'k-',lw=1.6)
ax.text(1.15,4.0,'2x₁ + x₂ − 6 = 0',fontsize=9)
ax.annotate('',xy=(3.3,1.4),xytext=(2.5,1.0),arrowprops=dict(arrowstyle='-|>',color=NAVY,lw=1.2))
ax.text(3.0,0.5,'w = (2, 1)',fontsize=8.5,color=NAVY)
ax.set_xlim(0,6); ax.set_ylim(0,4.6); ax.set_xlabel('x₁'); ax.set_ylabel('x₂'); ax.legend(fontsize=7.6,loc='upper right',frameon=False)
save(f,'linclf')

# --- confusion matrix 2x2 generic ---
f,ax=plt.subplots(figsize=(5.4,3.2)); ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,6.2)
ax.text(6.4,5.85,'Predicted class',ha='center',fontsize=10,fontweight='bold',color=NAVY)
ax.text(0.5,2.4,'Actual class',ha='center',va='center',rotation=90,fontsize=10,fontweight='bold',color=NAVY)
ax.text(4.6,5.25,'Positive',ha='center',fontsize=9); ax.text(8.2,5.25,'Negative',ha='center',fontsize=9)
ax.text(1.9,3.7,'Positive',ha='center',va='center',fontsize=9); ax.text(1.9,1.3,'Negative',ha='center',va='center',fontsize=9)
cells=[(4.6,3.7,'TP\nTrue Positive',GRN),(8.2,3.7,'FN\nFalse Negative\n(Type II error)',PNK),(4.6,1.3,'FP\nFalse Positive\n(Type I error)',PNK),(8.2,1.3,'TN\nTrue Negative',GRN)]
for x,y,t,fc in cells: box(ax,x,y,3.4,2.2,t,fc=fc,fs=9)
save(f,'cm2')

# --- multiclass confusion heatmap ---
M=np.array([[40,5,5],[4,30,6],[2,3,5]]); L=['Cat','Dog','Rabbit']
f,ax=plt.subplots(figsize=(3.8,3.2))
ax.imshow(M,cmap='Greys',vmin=-10,vmax=70)
for i in range(3):
    for j in range(3): ax.text(j,i,str(M[i,j]),ha='center',va='center',fontsize=11,color='white' if M[i,j]>25 else 'black',fontweight='bold' if i==j else 'normal')
ax.set_xticks(range(3)); ax.set_xticklabels(L); ax.set_yticks(range(3)); ax.set_yticklabels(L)
ax.set_xlabel('Predicted class'); ax.set_ylabel('Actual class')
for s in ax.spines.values(): s.set_visible(False)
save(f,'cm3')

# --- OvA and OvO ---
f,axs=plt.subplots(1,2,figsize=(7.2,3.0))
cent=[(2,2),(5.2,2.2),(3.6,5)]; mk=['o','^','s']; names=['A','B','C']
pts=[rng.normal(c,0.5,(14,2)) for c in cent]
for k,ax in enumerate(axs):
    for i in range(3): ax.scatter(*pts[i].T,c=C[i],marker=mk[i],s=18)
    for i,c in enumerate(cent): ax.text(c[0],c[1]-1.5 if i<2 else c[1]+1.25,f'Class {names[i]}',ha='center',fontsize=8.2,color=C[i],fontweight='bold')
    ax.set_xlim(0,7.2); ax.set_ylim(0,7.6); sc(ax)
ax=axs[0]; ax.set_title('(a) One-vs-All: 3 classifiers',fontsize=9.5)
ax.plot([3.4,3.4],[0,7.6],color=C[0],lw=1.3,ls='--'); ax.plot([3.8,3.8],[0,7.6],color=C[1],lw=1.3,ls='--'); ax.plot([0,7.2],[3.5,3.5],color=C[2],lw=1.3,ls='--')
ax.text(3.3,7.15,'A vs {B,C}',fontsize=7.6,color=C[0],ha='right'); ax.text(3.95,7.15,'B vs {A,C}',fontsize=7.6,color=C[1]); ax.text(5.3,3.65,'C vs {A,B}',fontsize=7.6,color=C[2])
ax=axs[1]; ax.set_title('(b) One-vs-One: 3 pairwise classifiers',fontsize=9.5)
ax.plot([3.6,3.6],[0,3.6],color='k',lw=1.3,ls='--'); ax.text(3.7,0.25,'A | B',fontsize=7.6)
ax.plot([0.2,3.6],[4.9,3.6],color='k',lw=1.3,ls='--'); ax.text(0.25,5.15,'A | C',fontsize=7.6)
ax.plot([3.6,7.0],[3.6,4.9],color='k',lw=1.3,ls='--'); ax.text(6.0,5.15,'B | C',fontsize=7.6)
f.tight_layout(); save(f,'ovaovo')
print('k1 done')
