import sys; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))  # padhai/scripts
from fig_lib import *
from matplotlib.patches import Circle as Ci
rng=np.random.default_rng(7)

# --- KNN concept ---
f,ax=plt.subplots(figsize=(4.2,3.3))
A=rng.normal([2.2,2.2],0.7,(12,2)); B=rng.normal([4.6,4.2],0.7,(12,2))
ax.scatter(*A.T,c=C[0],s=26,label='Class A'); ax.scatter(*B.T,c=C[1],marker='^',s=30,label='Class B')
q=np.array([2.9,3.3]); ax.scatter(*q,c='k',marker='*',s=150,zorder=5,label='New point ?')
d=np.sort(np.linalg.norm(np.vstack([A,B])-q,axis=1))
for k,ls in [(3,'-'),(7,'--')]:
    ax.add_patch(Ci(q,d[k-1]+0.04,fill=False,ls=ls,ec=NAVY,lw=1.1))
    ly=4.15 if k==3 else 4.75
    ax.annotate(f'K = {k}',xy=(q[0]-(d[k-1]+0.04)*0.94,q[1]+(d[k-1]+0.04)*0.34),xytext=(0.35,ly),fontsize=8.5,color=NAVY,
                arrowprops=dict(arrowstyle='-',color=NAVY,lw=0.8))
ax.set_xlim(0,7); ax.set_ylim(0,6.6); ax.set_aspect('equal'); ax.set_xlabel('Feature 1'); ax.set_ylabel('Feature 2')
ax.legend(fontsize=7.6,loc='upper right',frameon=False)
save(f,'knn'); 
nA=lambda k: sum(np.linalg.norm(A-q,axis=1)<=d[k-1]); print('K3 A',nA(3),'K7 A',nA(7))

# --- KNN numerical ---
f,ax=plt.subplots(figsize=(4.0,3.5))
X=np.array([[4,3],[6,7],[7,8],[5,5],[8,8]]); y=['Fail','Pass','Pass','Fail','Pass']
for (a,b),c in zip(X,y):
    ax.scatter(a,b,c=C[2] if c=='Pass' else C[4],marker='^' if c=='Pass' else 'o',s=50,zorder=3)
    off={(4,3):(0.2,-0.4),(6,7):(0.22,-0.42),(7,8):(-0.7,0.42),(5,5):(0.2,-0.4),(8,8):(0.22,-0.42)}[(a,b)]
    ax.text(a+off[0],b+off[1],f'({a},{b}) {c}',fontsize=8)
ax.scatter(6,8,c='k',marker='*',s=170,zorder=4); ax.annotate('Query (6, 8)',xy=(5.85,8.1),xytext=(2.7,9.45),fontsize=8.5,fontweight='bold',arrowprops=dict(arrowstyle='-|>',color=NAVY,lw=0.9))
ax.add_patch(Ci((6,8),2.05,fill=False,ec=NAVY,ls='--',lw=1.1)); ax.text(7.0,4.7,'circle radius = 2\n(contains the 3\nnearest neighbours)',fontsize=8,color=NAVY)
for (a,b),dd in [((6,7),'1'),((7,8),'1'),((8,8),'2')]:
    ax.plot([6,a],[8,b],color=GREY,lw=1,zorder=1)
ax.set_xlim(2.5,10.2); ax.set_ylim(1.8,10); ax.set_aspect('equal'); ax.set_xlabel('Physics (marks)'); ax.set_ylabel('Chemistry (marks)')
save(f,'knnnum')

# --- SVM numeric example ---
f,ax=plt.subplots(figsize=(4.6,3.4))
P=np.array([[3,1],[3,-1],[6,1],[6,-1]]); N=np.array([[1,0],[0,1],[0,-1],[-1,0]])
ax.axvspan(1,3,color=LG,zorder=0)
ax.scatter(*P.T,c=C[1],marker='^',s=55,label='Class +1',zorder=3); ax.scatter(*N.T,c=C[0],s=50,label='Class −1',zorder=3)
for s in [(1,0),(3,1),(3,-1)]: ax.scatter(*s,s=200,facecolors='none',edgecolors='k',lw=1.4,zorder=4)
ax.axvline(2,color='k',lw=1.6); ax.axvline(1,color='k',lw=1,ls='--'); ax.axvline(3,color='k',lw=1,ls='--')
ax.text(2,2.6,'x₁ − 2 = 0',fontsize=8.6,ha='center',bbox=dict(fc='white',ec='none',pad=1),zorder=6); ax.text(0.92,2.12,'w·x+b = −1',fontsize=8.2,ha='right'); ax.text(3.08,2.12,'w·x+b = +1',fontsize=8.2)
ax.annotate('',xy=(1,-1.95),xytext=(3,-1.95),arrowprops=dict(arrowstyle='<->',lw=1.1)); ax.text(2,-2.45,'margin = 2',fontsize=8.6,ha='center',bbox=dict(fc='white',ec='none',pad=1))
ax.text(4.2,-0.15,'circled = support vectors',fontsize=7.8)
ax.set_xlim(-2,7); ax.set_ylim(-2.75,2.95); ax.set_xlabel('x₁'); ax.set_ylabel('x₂'); ax.legend(fontsize=7.6,loc='lower right',frameon=False,bbox_to_anchor=(1.0,0.12))
save(f,'svm')

# --- hard vs soft ---
f,axs=plt.subplots(1,2,figsize=(7.2,3.0))
A=np.array([[1,1],[1.5,2],[2,0.8],[0.7,2.4],[1.8,1.6]]); B=np.array([[4,3.5],[4.6,2.6],[5,4],[4.2,4.6],[5.3,3]])
for ax in axs:
    ax.scatter(*A.T,c=C[0],s=30,zorder=3); ax.scatter(*B.T,c=C[1],marker='^',s=34,zorder=3)
    ax.set_xlim(0,6.4); ax.set_ylim(0,5.6); ax.set_xticks([]); ax.set_yticks([])
xx=np.linspace(0.3,6.2,10)
ax=axs[0]; ax.plot(xx,5.35-xx,'k-',lw=1.5); ax.plot(xx,3.5-xx,'k--',lw=1); ax.plot(xx,7.2-xx,'k--',lw=1)
for p in [(1.5,2),(4.6,2.6)]: ax.scatter(*p,s=150,facecolors='none',edgecolors='k',lw=1.2,zorder=4)
ax.set_title('(a) Hard margin: no point inside margin',fontsize=9.3)
ax=axs[1]; ax.scatter(3.6,2.7,c=C[0],s=30,zorder=3); ax.scatter(2.9,3.0,c=C[1],marker='^',s=34,zorder=3)
ax.plot(xx,5.35-xx,'k-',lw=1.5); ax.plot(xx,4.35-xx,'k--',lw=1); ax.plot(xx,6.35-xx,'k--',lw=1)
ax.annotate('ξ > 1: wrong side\n(misclassified)',xy=(3.68,2.62),xytext=(4.35,1.25),fontsize=7.6,bbox=dict(fc='white',ec='none',pad=0.6),arrowprops=dict(arrowstyle='-|>',color=NAVY,lw=0.9))
ax.annotate('0 < ξ < 1: correct side\nbut inside margin',xy=(2.88,2.92),xytext=(2.3,0.25),fontsize=7.6,bbox=dict(fc='white',ec='none',pad=0.6),arrowprops=dict(arrowstyle='-|>',color=NAVY,lw=0.9))
ax.set_title('(b) Soft margin: slack ξ allows violations',fontsize=9.3)
f.tight_layout(); save(f,'soft')

# --- kernel trick: 1D -> 2D ---
f,axs=plt.subplots(1,2,figsize=(7.0,2.6))
x_in=np.array([-1,-0.6,-0.3,0,0.3,0.6,1.0]); x_out=np.array([-3,-2.5,-2,2,2.5,3])
ax=axs[0]; ax.scatter(x_in,0*x_in,c=C[0],s=34,zorder=3); ax.scatter(x_out,0*x_out,c=C[1],marker='^',s=38,zorder=3)
ax.axhline(0,color=GREY,lw=0.8); ax.set_yticks([]); ax.set_xlim(-3.5,3.5); ax.set_ylim(-1,1); ax.set_title('(a) Input space x: no single line separates',fontsize=9.2); ax.set_xlabel('x')
ax=axs[1]; ax.scatter(x_in,x_in**2,c=C[0],s=34,zorder=3); ax.scatter(x_out,x_out**2,c=C[1],marker='^',s=38,zorder=3)
ax.axhline(2.5,color='k',ls='--',lw=1.3); ax.text(-3.3,2.85,'linear boundary x² = 2.5',fontsize=8)
ax.set_xlim(-3.5,3.5); ax.set_ylim(-0.5,10); ax.set_xlabel('x'); ax.set_ylabel('x²'); ax.set_title('(b) Feature space φ(x) = (x, x²): separable',fontsize=9.2)
f.tight_layout(); save(f,'ktrick')

# --- kernel curves ---
f,axs=plt.subplots(1,2,figsize=(7.0,2.7))
r=np.linspace(0,4,200); ax=axs[0]
for g,c in [(0.1,C[0]),(0.5,C[1]),(2,C[2])]: ax.plot(r,np.exp(-g*r**2),color=c,lw=1.6,label=f'γ = {g}')
ax.set_xlabel('distance ‖x − z‖'); ax.set_ylabel('K(x, z)'); ax.set_title('(a) RBF / Gaussian: similarity decays',fontsize=9.2); ax.legend(fontsize=7.8,frameon=False)
t=np.linspace(-3,3,200); ax=axs[1]
ax.plot(t,(t+1)**2/4,color=C[0],lw=1.6,label='Polynomial (t+1)² / 4'); ax.plot(t,t,color=GREY,lw=1.2,ls=':',label='Linear t')
ax.plot(t,np.tanh(t),color=C[4],lw=1.6,label='Sigmoid tanh(t)')
ax.set_xlabel('t = x · z'); ax.set_title('(b) Dot-product kernels',fontsize=9.2); ax.legend(fontsize=7.6,frameon=False,loc='upper left'); ax.set_ylim(-1.6,4.2)
f.tight_layout(); save(f,'kcurves')

# --- regression residuals ---
f,ax=plt.subplots(figsize=(4.2,3.0))
xs=np.array([1,2,3,4,5,6.]); ys=np.array([2.2,2.8,4.6,4.4,6.1,6.4]); bb,aa=np.polyfit(xs,ys,1)
ax.scatter(xs,ys,c=C[0],s=32,zorder=3,label='Actual yᵢ'); ax.plot([0.5,6.5],[aa+bb*0.5,aa+bb*6.5],'k-',lw=1.4,label='Fitted line ŷ')
for xi,yi in zip(xs,ys): ax.plot([xi,xi],[yi,aa+bb*xi],color=C[4],lw=1.2)
ax.text(3.15,3.55,'eᵢ = yᵢ − ŷᵢ',fontsize=8.6,color=C[4]); ax.legend(fontsize=7.8,frameon=False,loc='upper left')
ax.set_xlabel('x'); ax.set_ylabel('y'); save(f,'resid')

# --- Bayesian prior / posterior ---
f,ax=plt.subplots(figsize=(4.6,2.9))
w=np.linspace(-3,4,400); g=lambda m,v: np.exp(-(w-m)**2/(2*v))/np.sqrt(2*np.pi*v)
ax.plot(w,g(0,1),color=GREY,lw=1.6,ls='--',label='Prior  N(0, 1)'); ax.plot(w,g(4/3,1/6),color=C[0],lw=1.8,label='Posterior  N(1.33, 0.167)')
ax.axvline(1.6,color=C[4],lw=1.2,ls=':'); ax.text(1.68,0.86,'OLS = 1.6',fontsize=8.2,color=C[4])
ax.set_xlabel('weight w'); ax.set_ylabel('density'); ax.legend(fontsize=7.8,frameon=False,loc='upper left'); ax.set_ylim(0,1.12)
save(f,'bayes')
print('k2 done')
