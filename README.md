dvcfg2oto
=========
About 
-----
> (EN)Converts deepvocal's `voice.dvcfg` to utau's `oto.ini` (supports CV, VX, INDIE all)<br>
> (KO)딥보컬의 `voice.dvcfg`를 우타우의 `oto.ini`로 변환하는 프로그램입니다. CV/VX/INDIE 모두 변환 가능합니다.<br><br>
> ![image](https://user-images.githubusercontent.com/100339835/202849838-ba9ba007-39ba-42b5-8dcc-a43d5189f1bd.png)
#### 
How To Use
----------
> (EN)**1. Select your folder.** Folder must have `'voice.dvcfg'`, or conversion never starts.<br>
> (KO)**1. 폴더를 선택하세요.** `voice.dvcfg`가 폴더 내에 포함되어 있지 않을 경우, 변환 버튼이 활성화되지 않습니다.<br><br>
> ![image](https://user-images.githubusercontent.com/100339835/202850317-e8904826-2704-4de7-99e4-d86b4043c5ab.png)
#### 
#### 
> (EN) **2. Push 'Convert' button.**<br>
> (KO) **2. 'Convert'를 누르세요.**<br><br>
> ![image](https://user-images.githubusercontent.com/100339835/202850568-fac10c6c-cacc-401b-bc3d-96dfc8db04a0.png)
#### 
####
> (EN) **+. You can edit `dict.txt` .** <br> For example: if `ga=가` in `dict.txt`, `-ga` or `ga` will be converted into `- 가` or `가`.<br>
> (KO) **+. `dict.txt`를 임의로 커스텀할 수 있습니다.** <br> `dict.txt`에 `ga=가`로 입력되어 있을 경우, `-ga`와 `ga`는 `- 가`와 `가`로 변환됩니다. 
#### 
### (EN) About `setting.ini`
> dvcfg encoding = encoding of `voice.dvcfg`<br>
> oto encoding = encoding of `oto.ini`<br>
> backup existing oto = if `yes`, backups `oto.ini` into `oto_original.ini`. if `no`, it does not backups `oto.ini`<br>
> overlap factor = default value is `0.15`.<br>
### (KO) `setting.ini`에 대하여
> dvcfg encoding = `voice.dvcfg`의 인코딩<br>
> oto encoding = `oto.ini`의 인코딩<br>
> backup existing oto = `yes`로 설정되어 있을 경우, `oto.ini`가 이미 존재할 때 해당 `oto.ini`를 `oto_original.ini`로 백업합니다. `no`일 경우 `oto.ini`를 백업하지 않고 덮어씁니다. <br>
> overlap factor = 기본값은 `0.15`입니다.<br>
### 
Download
--------
> (EN)Go to Release.<br>
> (KO)Release 란을 참고하세요.
#### 
Reference
---------
#### [Kahsolt/dvcfg2oto](https://github.com/Kahsolt/dvcfg2oto.git)
