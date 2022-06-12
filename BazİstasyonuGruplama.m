    %% 10:10 Alanı Çizdirme
close all; clc; clear;
x1=-5;
x2=5;
y1=-5;
y2=5;
x = [x1, x2 , x2,x1,x1];
y = [y1, y1 , y2 ,y2,y1];
plot(x, y, 'b-', 'LineWidth', 3);
axis([-7 7 -7 7]);
grid on , hold on
% Random 10 cihazın alan içine bırakılması
 
for i= 1:12
    if rand(1)<0.5
        X(i)= rand(1)*5;
        Y(i)= rand(1)*5;
    else
         X(i)=-rand(1)*5;
         Y(i)=-rand(1)*5;
    end
    text(X(i)+0.15,Y(i)-0.15,num2str(i))
    noktalar(i,1)=X(i);
    noktalar(i,2)=Y(i);
end
scatter(X,Y,'filled', 'LineWidth' , 2)

%% Baz İstasyonu Koyulması
sbtguc=0;
sbtistasyonx = [0];
sbtistasyony = [0];
scatter(sbtistasyonx,sbtistasyony,'x', 'LineWidth' ,2)
for i=1:12
    mesafe= sqrt((X(i)-sbtistasyonx)^2+(Y(i)-sbtistasyony)^2);
    sbtguc= sbtguc + mesafe^2;
end
text(0.25,0,'Sabit Baz İstasyonu')


%% optimum baz istasyonu
ortx=0;orty =0;optguc=0;
for i=1:12
    ortx = ortx + X(i);
    orty = orty + Y(i);
end
ortx = ortx/12; orty=orty/12;
scatter(ortx,orty,'x', 'LineWidth' ,2)
text(ortx+0.25,orty,'Optimum Baz İstasyonu')

for i=1:12
    mesafe= sqrt((X(i)-ortx)^2+(Y(i)-orty)^2);
    optguc= optguc + mesafe^2;
end




%% Noktaların diğer noktalara olan uzaklığını tutan 12 ye 12 matrisin çıkarılması ve sıralanması
for i=1:12 %1.satır 1.noktanın 2.satır 2.noktanın diğerlerine olan uzaklığı şeklinde ilerliyor
    for k=1:12
     gelistirme(i,k)= sqrt((X(i)-X(k))^2+(Y(i)-Y(k))^2);
    end
end

siralama = gelistirme(:,:);
tutucu=0;
for z=1:12
for k=1:11
    for i=1:12
    if siralama(i,k)>siralama(i,k+1)
        tutucu = siralama(i,k);
        siralama(i,k) =siralama(i,k+1);
        siralama(i,k+1)=tutucu;
    end
    end
end
end
%% Grup tabanı için birbiri için en yakın olan noktaları eşleştirme
grup = zeros (12 ,6);
c=1; l=1;
for t=1:12
    for y=1:11
        if siralama(t,2)== siralama(y,2)
            if t==y
                continue
            else
            l=1;
           while l<5
               if l==1
               grup(c,l)=X(t);
               end
               if l==2
                   grup(c,l)=Y(t);
               end
                if l==3
                   grup(c,l)=X(y);
                end
                if l==4
                   grup(c,l)=Y(y);     %% tüm mesafeleri tek satıra al 
                end
               l=l+1;
           end
           c=c+1;
            end
          
            end
     end
end     

%% Matris simetrik olduğu için aynı anlama gelen grupları silme ve matrisi düzenleme
for i=1:12
    for k=1:12
        if grup(i,1)==grup(k,3)
            grup(k,:)=0;
        end
    end
end

for z=1:6
for k=1:6
    for i=1:11
        if grup(i,k)==0
            tutucu = grup(i,k);
            grup(i,k)=grup(i+1,k);
            grup(i+1,k)=tutucu;         
            
        end
    end
end
end
% 
mesafe = zeros(4,12);
for i=1:12
    if grup(1,1)==X(i) | grup(1,3)==X(i) | grup(2,1)==X(i) | grup(2,3)==X(i)| grup(3,1)==X(i) | grup(3,3)==X(i)| grup(4,1)==X(i) | grup(4,3)==X(i)
        mesafe(1,i)=0;
        mesafe(2,i)=0;
        mesafe(3,i)=0;
        mesafe(4,i)=0;
    else
    mesafe(1,i)= sqrt((grup(1,1)-X(i))^2+(grup(1,2)-Y(i))^2)+(sqrt((grup(1,3)-X(i))^2+(grup(1,4)-Y(i))^2));
    mesafe(2,i)= sqrt((grup(2,1)-X(i))^2+(grup(2,2)-Y(i))^2)+(sqrt((grup(2,3)-X(i))^2+(grup(2,4)-Y(i))^2));
    mesafe(3,i)= sqrt((grup(3,1)-X(i))^2+(grup(3,2)-Y(i))^2)+(sqrt((grup(3,3)-X(i))^2+(grup(3,4)-Y(i))^2));
    mesafe(4,i)= sqrt((grup(4,1)-X(i))^2+(grup(4,2)-Y(i))^2)+(sqrt((grup(4,3)-X(i))^2+(grup(4,4)-Y(i))^2));

end
end
for i=1:12
 if grup(3,2)==0
     mesafe(3,i)=0;
     mesafe(4,i)=0;
 end
end
%%
sayan = zeros(1,4);
tutucu=25;
for i=1:12
  if (mesafe(1,i)~=0) &  (mesafe(1,i)<tutucu)
      tutucu = mesafe(1,i);
      sayan(1,1)=i;
  end
end

tutucu=25;
for i=1:12
  if (mesafe(2,i)~=0) &  (mesafe(2,i)<tutucu)
      tutucu = mesafe(2,i);
      sayan(1,2)=i;
  end
end

tutucu=25;
for i=1:12
  if (mesafe(3,i)~=0) &  (mesafe(3,i)<tutucu)
      tutucu = mesafe(3,i);
      sayan(1,3)=i;
  end
end

tutucu=25;
for i=1:12
  if (mesafe(4,i)~=0) &  (mesafe(4,i)<tutucu)
      tutucu = mesafe(4,i);
      sayan(1,4)=i;
  end
end
%% mesafeyi sıralama
uzunluk = mesafe(:,:);
tutucu=0;
for z=1:12
for k=1:11
    for i=1:4
    if uzunluk(i,k)>uzunluk(i,k+1)
        tutucu = uzunluk(i,k);
        uzunluk(i,k) =uzunluk(i,k+1);
        uzunluk(i,k+1)=tutucu;
        
    end
    end
end
end
%% Eşit gelen değerlerden toplamı daha küçük olanı sayana atıp diğerini bir sonraki en küçük değere koyma
for k=1:4
   for i=1:4
       if sayan(1,k)== sayan(1,i)
           if i==k
           else
           esit(1,1)=i;
           esit(1,2)=k;
           if mesafe(i,sayan(1,i)) < mesafe(k,sayan(1,k))
              for m=1:11
                  if uzunluk(k,m)==0
                  else
                  xc=uzunluk(k,m+1);
                  break
                  end
              end
              for n=1:12
                  if mesafe(k,n)== xc   
                     sayan(1,k)=n;
                  end
              end
              if mesafe(i,sayan(1,i)) > mesafe(k,sayan(1,k))
                 for m=1:11
                     if uzunluk(i,m)==0
                     else
                     xc=uzunluk(i,m+1);
                     break
                     end
                 end
                 for n=1:12
                     if mesafe(i,n)== xc   
                        sayan(1,i)=n;
                     end
                 end
              end
           end
           end
       end
   end
end
% EGER DEGİSTİRLEN SAYI ONCDEDEN ESİT OLMAYAN BİR SAYIYA ESİTLENDİYSE Bİ
% TUR DAHA DON
%%
for t=1:4
    for y=1:4
        if sayan(1,t)== sayan(1,y)
            if y==t
            else
            esit(1,1)=y;
            esit(1,2)=t;
            if mesafe(y,sayan(1,y)) < mesafe(t,sayan(1,t))
                for m=1:10
                    if uzunluk(t,m)==0
                    else
                    xc=uzunluk(t,m+2);
                    break
                    end
                end
                    for n=1:12
                        if mesafe(t,n)== xc   
                            sayan(1,t)=n;
                        end
                    end
                    if mesafe(y,sayan(1,y)) > mesafe(y,sayan(1,y))
                        for m=1:10
                            if uzunluk(i,m)==0
                            else
                            xc=uzunluk(i,m+2);
                            break
                            end
                        end
                        for n=1:12
                            if mesafe(i,n)== xc   
                               sayan(1,y)=n;
                            end
                        end
                    end
                end
            end
        end
    end
end
%%
k=0;
while k<8
    grup(5,:)=[];
    k=k+1;
    
end
grup(1,5)=noktalar(sayan(1,1),1);
grup(1,6)=noktalar(sayan(1,1),2);

if grup(2,4)~=0
grup(2,5)=noktalar(sayan(1,2),1);
grup(2,6)=noktalar(sayan(1,2),2);
end

if grup(3,4)~=0
grup(3,5)=noktalar(sayan(1,3),1);
grup(3,6)=noktalar(sayan(1,3),2);
end

if grup(4,4) ~=0
grup(4,5)=noktalar(sayan(1,4),1);
grup(4,6)=noktalar(sayan(1,4),2);
end

grup

%% Bosta Kalan Noktaları Son Gruba Koyma

h = 1;
if grup(4,1)==0
for i=1:12
    if noktalar(i,1)~=grup(1,1) & noktalar(i,1)~=grup(1,3) & noktalar(i,1)~=grup(1,5) & noktalar(i,1)~=grup(2,1) &noktalar(i,1)~=grup(2,3) & noktalar(i,1)~=grup(2,5)& noktalar(i,1)~=grup(3,1) & noktalar(i,1)~=grup(3,3) & noktalar(i,1)~=grup(3,5)
    grup(4,h)=noktalar(i,1);grup(4,h+1)=noktalar(i,2);
    h=h+2;
    
    end
end
end
%% Güç Ölçümü

guc(1,1)= abs((grup(1,1)-grup(1,3))^2+(grup(1,2)-grup(1,4)^2)); %1 ile 2 nin arasındaki mesafe
guc(1,2)= abs((grup(1,1)-grup(1,5))^2+(grup(1,2)-grup(1,6)^2)); %1 ile 3 arasındaki mesafe
guc(1,3)= abs((grup(1,3)-grup(1,5))^2+(grup(1,4)-grup(1,6)^2)); %2 ile 3 arasındaki mesafe
for i=1:2:5
    hesapla=((grup(1,i)-ortx)^2+(grup(1,i+1)-orty)^2);
    if hesapla < ((grup(1,3)-ortx)^2+(grup(1,4)-orty)^2)
        guc(1,4) = hesapla;
    else
        guc(1,4) = ((grup(1,3)-ortx)^2+(grup(1,4)-orty)^2);
    end
end

        


guc(2,1)= abs((grup(2,1)-grup(2,3))^2+(grup(2,2)-grup(2,4)^2)); %1 ile 2 nin arasındaki mesafe
guc(2,2)= abs((grup(2,1)-grup(2,5))^2+(grup(2,2)-grup(2,6)^2)); %1 ile 3 arasındaki mesafe
guc(2,3)= abs((grup(2,3)-grup(2,5))^2+(grup(2,4)-grup(2,6)^2)); %2 ile 3 arasındaki mesafe
for i=1:2:5
    hesapla=((grup(2,i)-ortx)^2+(grup(2,i+1)-orty)^2);
    if hesapla < ((grup(2,3)-ortx)^2+(grup(2,4)-orty)^2)
        guc(2,4) = hesapla;
    else
        guc(2,4) = ((grup(2,3)-ortx)^2+(grup(2,4)-orty)^2);
    end
end

guc(3,1)= abs((grup(3,1)-grup(3,3))^2+(grup(3,2)-grup(3,4)^2)); %1 ile 2 nin arasındaki mesafe
guc(3,2)= abs((grup(3,1)-grup(3,5))^2+(grup(3,2)-grup(3,6)^2)); %1 ile 3 arasındaki mesafe
guc(3,3)= abs((grup(3,3)-grup(3,5))^2+(grup(3,4)-grup(3,6)^2)); %2 ile 3 arasındaki mesafe
for i=1:2:5
    hesapla=((grup(3,i)-ortx)^2+(grup(3,i+1)-orty)^2);
    if hesapla < ((grup(3,3)-ortx)^2+(grup(3,4)-orty)^2)
        guc(3,4) = hesapla;
    else
        guc(3,4) = ((grup(3,3)-ortx)^2+(grup(3,4)-orty)^2);
    end
end

guc(4,1)= abs((grup(4,1)-grup(4,3))^2+(grup(4,2)-grup(4,4)^2)); %1 ile 2 nin arasındaki mesafe
guc(4,2)= abs((grup(4,1)-grup(4,5))^2+(grup(4,2)-grup(4,6)^2)); %1 ile 3 arasındaki mesafe
guc(4,3)= abs((grup(4,3)-grup(4,5))^2+(grup(4,4)-grup(4,6)^2)); %2 ile 3 arasındaki mesafe
for i=1:2:5
    hesapla=((grup(4,i)-ortx)^2+(grup(4,i+1)-orty)^2);
    if hesapla < ((grup(4,3)-ortx)^2+(grup(4,4)-orty)^2)
        guc(4,4) = hesapla;
    else
        guc(4,4) = ((grup(4,3)-ortx)^2+(grup(4,4)-orty)^2);
    end
end
toplamguc = sum(sum(guc));

figure,
bar(0,sbtguc)
hold on
bar(1,optguc)
title('Grafiksel Karşılaştırma')
bar(2,toplamguc)
%% LEACH PROTOCOL
for i=1:12
    nokta(i).x = noktalar(i,1);
    nokta(i).y = noktalar(i,2);
    if rand < 0.60
        nokta(i).clusterhead = 0;
    else
        nokta(i).clusterhead = 1;
    end
end
absdistance = zeros(1,12)
for i=1:12
    if nokta(i).clusterhead == 0
        absdistance(i) = (nokta(i).x-ortx)^2+(nokta(i).x-orty^2);
       for k=1:12
           if nokta(k).clusterhead == 1
               distance = (nokta(i).x-nokta(k).x)^2+(nokta(i).x-nokta(k).y)^2;
               if distance < absdistance
                  absdistance(i) = distance;              
               end       
           end
       end
    else
        absdistance(i) = (nokta(i).x-ortx)^2+(nokta(i).x-orty^2);
    end
end
              
leach=sum(absdistance)
bar(3,leach)
              






















