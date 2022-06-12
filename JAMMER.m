%%ALDATICI JAMMERE KARŞI
zaman=7;
%degisenkod=280;
%%
bilgi=[1 0 1 1 1 0 0 1 0 0];
sifreli_kod=bilgi;
cevap = input('radar calissin mi? Y/N [Y]:','s');
       if isempty(cevap)
          zaman=zaman+1;
       end
if isempty(cevap)
    for i=1:mod(zaman,length(bilgi))
         if bilgi(i)==1
            sifreli_kod(i)=0;
         else
            sifreli_kod(i)=1;
         end
    end
    if mod(zaman,7) == 3;
        sifreli_kod(mod(zaman,7))=1;
    else
        for i=1:mod(zaman,length(bilgi))
             if bilgi(mod(zaman+4,7))== 1;
                sifreli_kod(mod(zaman+4,7))=0;
             else
             end
        end
    end
else
end
%%
%Tasiyici isaretin uretimi
Tb=1; t=0:Tb/100:1;
fc=2.4e9;
c=10*sin(2*pi*fc*t); %Tasiyici isaretinin uretimi

c_awgn=awgn(c,0,'measured'); %taşıyıcıya 0db beyaz gürültü eklendi

t1=0; t2=Tb;
for i=1:length(bilgi)
    t=[t1:.01:t2];
    if sifreli_kod(i)>0.5
       sifreli_kod(i)=1;
       m_s=ones(1,length(t));
    else sifreli_kod(i)=0;
       m_s=zeros(1,length(t));
    end
    message(i,:)=m_s;
    %Tasiyici ve bilginin uretimi
    m_awgn=awgn(message(i,:),20,'measured');
    ask_sig(i,:)=c_awgn.*m_awgn;
    t1=t1+(Tb+.01);
    t2=t2+(Tb+.01);
    %Bilgi ve ASK isaretinin cizdirimi
    subplot(5,1,2);axis([0 9 -2 2]);plot(t,m_awgn,'r');
    title('Bilgi isareti');xlabel('t−−−>');ylabel('m(t)');grid on; hold on
     
     subplot(5,1,4);plot(t,ask_sig(i,:));
     title('ASK isareti');xlabel('t−−−>');ylabel('s(t)');grid on; hold on
end
hold off
%Tasiyici isaret ve ikili giris verisinin cizdirimi
subplot(5,1,3);plot(t,c_awgn);
title('Tasiyici isaret');xlabel('t−−−>');ylabel('c(t)');grid on
subplot(5,1,1);stem(sifreli_kod);
title('Ikili veri bitleri');xlabel('n−−−>');ylabel('b(n)');grid on

%ASK Demodulasyonu
Tb=1;
t1=0;t2=Tb;
for i=1:length(bilgi)
t=[t1:Tb/100:t2];
%Korelasyon
x=sum(c_awgn.*ask_sig(i,:));
%Karar araci
if x>0
demod(i)=1;
else demod(i)=0;
end
t1=t1+(Tb+.01);
t2=t2+(Tb+.01);
end
%Demoduleli ikili veri bitlerinin cizdirimi
subplot(5,1,5); stem(demod);
title('ASK demoduleli isaret'); xlabel('n−−−>');ylabel('b(n)');grid on
%%
demod = [0,1,0,0,0,1,1,0,0,0];
%% düzeltme

demod_yedek=demod; %sifreli kodun kopyasi
cozulmus_kod=demod;
for i=1:mod(zaman,length(demod))
         if demod(i)==0
            cozulmus_kod(i)=1;
         else
            cozulmus_kod(i)=0;
         end
    end
     if mod(zaman,7) == 3;
        sifreli_kod(mod(zaman,7))=1;
    else
        for i=1:mod(zaman,length(demod))
             if demod(mod(zaman+4,7))== 0;
                cozulmus_kod(mod(zaman+4,7))=1;
             else
             end
        end
    end

%% iterasyon
degisenkod_gel=zaman;
h=1;
while(h)
if cozulmus_kod==bilgi
    disp('bilgi basariyla alindi')
    h=0; 
else
    demod=demod_yedek;
    zaman=zaman+1
    if zaman > degisenkod_gel+256
        disp('bilgi hatali veya aldatici jammer var')
        h=0;
    else
    end
for i=1:mod(zaman,length(demod))
         if demod(i)==0
            cozulmus_kod(i)=1;
         else
            cozulmus_kod(i)=0;
         end
    end
     if mod(zaman,7) == 3;
        sifreli_kod(mod(zaman,7))=1;
    else
        for i=1:mod(zaman,length(demod))
             if demod(mod(zaman+4,7))== 0;
                cozulmus_kod(mod(zaman+4,7))=1;
             else
             end
        end
    end
end 
end
%% NOİSE JAMMER
Fs=100;Ts=1/Fs;
t=0:Ts:2;
x=20*cos(2*pi*20*t)+10*sin(2*pi*20*t);
tasiyici1=cos(2*pi*20*t);


x_g=awgn(x,0 ,'measured');
subplot(2,1,1)
plot(t,x),title('x(t) işareti'),xlabel('Zaman [sn]'),ylabel('Genlik [V]');
subplot(2,1,2)
plot(t,x_g,'r'),title('0dB gürültülü x(t) işareti'),xlabel('Zaman [sn]'),ylabel('Genlik [V]');

figure
mag_Z = fftshift(abs(fft(x_g)));mag_Z = 1/numel(mag_Z)*mag_Z;
F1 = linspace(-Fs/2,Fs/2,numel(mag_Z));
plot(F1,mag_Z,'r'),grid on;
xlabel('Frekans [Hz]'),ylabel('Genlik [V]')
title('0 dB gürültülü |X(jw)| işareti');
%%
sinyal=tasiyici1.*x;
sinyal=awgn(sinyal,0 ,'measured');
mag_S = fftshift(abs(fft(sinyal)));mag_S = 1/numel(mag_S)*mag_S;
F2 = linspace(-Fs/2,Fs/2,numel(mag_S));
plot(F2,mag_S,'r'),grid on;
xlabel('Frekans [Hz]'),ylabel('Genlik [V]')
title('Tasiyicili Sinyal işareti');

%%
barragejammer = barrageJammer('ERP',1000,'SamplesPerFrame',201);
jammer=step(barragejammer);
jammer=jammer';
mag_X = fftshift(abs(fft(jammer)));mag_X = 1/numel(mag_X)*mag_X;
subplot(2,1,1)
plot(t,jammer),title('Jammer Zaman Domeni');
subplot(2,1,2)
plot(F2,mag_X,'r'),grid on;
title(' |jammer(jw)| işareti');
alici=jammer+sinyal;

figure
subplot(2,1,1)
    plot(t,alici),title('Jammer Sonrasi olusan yeni sinyal');
    mag_X2 = fftshift(abs(fft(alici)));mag_X2 = 1/numel(mag_X2)*mag_X2;
    subplot(2,1,2)
plot(F2,mag_X2,'r'),grid on;
title('Genlik Spektrumue');
 
 
    