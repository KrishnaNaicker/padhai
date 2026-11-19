import numpy as np
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
print("== KNN ==")
X=np.array([[4,3],[6,7],[7,8],[5,5],[8,8]]); y=['Fail','Pass','Pass','Fail','Pass']
q=np.array([6,8])
for (a,b),c in zip(X,y):
    d2=(a-q[0])**2+(b-q[1])**2; print(a,b,c,d2,round(np.sqrt(d2),3))
for k in (1,3,5):
    print(k, KNeighborsClassifier(n_neighbors=k).fit(X,y).predict([q]))
print("== CM 2x2 ==")
for name,(TP,FP,FN,TN) in {"A: actual=cols":(45,18,12,25),"B: actual=rows":(45,12,18,25)}.items():
    acc=(TP+TN)/100; P=TP/(TP+FP); R=TP/(TP+FN); F=2*P*R/(P+R); S=TN/(TN+FP)
    print(name,TP,FP,FN,TN,acc,round(P,4),round(R,4),round(F,4),'spec',round(S,4),'err',1-acc,'FPR',round(FP/(FP+TN),4))
print("== imbalance ==")
print("acc all-neg", 990/1000)
print("== multiclass ==")
M=np.array([[40,5,5],[4,30,6],[2,3,5]])  # rows actual, cols predicted
yt=[];yp=[]
for i in range(3):
    for j in range(3): yt+= [i]*M[i,j]; yp+=[j]*M[i,j]
for avg in (None,'macro','micro','weighted'):
    print(avg, [np.round(v,4) for v in precision_recall_fscore_support(yt,yp,average=avg)[:3]])
print('acc',np.trace(M)/M.sum(), M.sum(), M.sum(0), M.sum(1))
print("== SVM ==")
Xs=np.array([[3,1],[3,-1],[6,1],[6,-1],[1,0],[0,1],[0,-1],[-1,0]]); ys=[1,1,1,1,-1,-1,-1,-1]
m=SVC(kernel='linear',C=1e6).fit(Xs,ys); print('w',m.coef_,'b',m.intercept_,'sv',m.support_vectors_,'alpha',m.dual_coef_)
w=m.coef_[0]; print('margin',2/np.linalg.norm(w)); print('f(4,2)',w@[4,2]+m.intercept_, 'f(1.5,0)',w@[1.5,0]+m.intercept_)
print("== kernels ==")
x=np.array([1,2]); z=np.array([2,3])
print('lin',x@z,'poly d2 c1',(x@z+1)**2,'poly d2 c0',(x@z)**2,'rbf g0.5',np.exp(-0.5*np.sum((x-z)**2)),'gauss s1',np.exp(-np.sum((x-z)**2)/2),'sig',np.tanh(0.1*(x@z)+0), np.tanh(0.1*8-1))
phi=lambda v: np.array([v[0]**2,np.sqrt(2)*v[0]*v[1],v[1]**2]); print('phi dot',phi(x)@phi(z))
print("== MSE ==")
s=13.33+3.33+4.00; print('SSE',s,'MSE/100',s/100,'RMSE',np.sqrt(s/100),'MSE/3',s/3,np.sqrt(s/3))
print("== Bayes ==")
xb=np.array([1,2.]); yb=np.array([2,3.]); a=1; s2=1
prec=a+xb@xb/s2; mn=(xb@yb/s2)/prec; print('post prec',prec,'mean',mn,'var',1/prec,'ols',xb@yb/(xb@xb))
xs=3; print('pred mean',mn*xs,'pred var',s2+xs**2/prec, np.sqrt(s2+xs**2/prec))
print("== linear clf ==")
w=np.array([2,1]); b=-6
for p in [(4,3),(1,1),(2,2),(3,0)]: print(p, w@p+b)
