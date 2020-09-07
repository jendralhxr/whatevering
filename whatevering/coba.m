# plot 8 IMFS, and original signal
for i=1:8
	subplot(3,3,i);
	plot(em1610c1(:,i));
endfor
subplot(3,3,9);
plot(raw1610cc(:,1));
print -dpsc /me/1610cc1.eps;

for i=1:8
	subplot(3,3,i);
	plot(em1610c2(:,i));
endfor
subplot(3,3,9);
plot(raw1610cc(:,2));
print -dpsc /me/1610cc2.eps;

for i=1:8
	subplot(3,3,i);
	plot(em1610c3(:,i));
endfor
subplot(3,3,9);
plot(raw1610cc(:,3));
print -dpsc /me/1610cc3.eps;

for i=1:8
	subplot(3,3,i);
	plot(em1610c4(:,i));
endfor
subplot(3,3,9);
plot(raw1610cc(:,4));
print -dpsc /me/1610cc4.eps;

for i=1:8
	subplot(3,3,i);
	plot(em1610c5(:,i));
endfor
subplot(3,3,9);
plot(raw1610cc(:,5));
print -dpsc /me/1610cc5.eps;

for i=1:8
	subplot(3,3,i);
	plot(em1610c6(:,i));
endfor
subplot(3,3,9);
plot(raw1610cc(:,6));
print -dpsc /me/1610cc6.eps;

for i=1:8
	subplot(3,3,i);
	plot(em1610c7(:,i));
endfor
subplot(3,3,9);
plot(raw1610cc(:,7));
print -dpsc /me/1610cc7.eps;

for i=1:8
	subplot(3,3,i);
	plot(em1610v1(:,i));
endfor 
subplot(3,3,9); 
plot(raw1610dic(:,1)); 
print -dpsc /me/1610dic1.eps;

for i=1:8
	subplot(3,3,i);
	plot(em1610v2(:,i));
endfor
subplot(3,3,9);
plot(raw1610dic(:,2));
print -dpsc /me/1610dic3.eps;

for i=1:8
	subplot(3,3,i);
	plot(em1610v3(:,i));
endfor
subplot(3,3,9);
plot(raw1610dic(:,3));
print -dpsc /me/1610dic5.eps;

for i=1:8
	subplot(3,3,i);
	plot(em1610v4(:,i));
endfor
subplot(3,3,9);
plot(raw1610dic(:,4));
print -dpsc /me/1610dic7.eps;
