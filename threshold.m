STF=36000;

threshold=3; # mm
displacement_thre(size(displacement,1), 7)=0; 
#for j=1:size(displacement,1)
for j=STF:size(displacement,1)
 for i=2:8
  temp= displacement(j,i);
  if (temp<threshold) && (temp>-threshold)
   displacement_thre(j,i-1)= 0;
  else 
   displacement_thre(j,i-1)= abs(displacement(j,i));
   #displacement_thre(j,i-1)= abs(displacement(j,i));
  endif
 endfor
endfor
plot(displacement_thre(:,4));

