import sys
import json
import wave
import shutil
from pathlib import Path
from configparser import ConfigParser
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
from PyQt5 import uic
from PyQt5.QtGui import QIcon

def open_(fp, rw='r', **kwargs):
  return open(fp, rw, encoding=file_encoding, **kwargs)

def get_duration(fp) -> float:
  with wave.open(fp) as wav:
    return wav.getnframes() / wav.getframerate()

#check setting_ini
dvcfg_filename = 'voice.dvcfg'
oto_filename = 'oto.ini'

config = ConfigParser()
config.read('setting.ini', encoding='utf-8')



if config == []:
    with open('setting.ini') as configfile:
        config.add_section("DEFAULT")
        config.set("DEFAULT", 'dvcfg encoding', 'utf-8')
        config.set("DEFAULT", 'oto encoding', 'utf-8')
        config.set("DEFAULT", 'backup exsisting oto', 'yes')
        config.set("DEFAULT", 'overlap factor', '0.15')
        config.write(configfile)
else:
    if not 'dvcfg encoding' in config:
        config.set("DEFAULT", 'dvcfg encoding', 'utf-8')
    if not 'oto_encoding' in config:
        config.set("DEFAULT", 'oto encoding', 'utf-8')
    if not 'backup existing oto' in config:
        config.set("DEFAULT", 'backup existing oto', 'yes')
    if not 'overlap factor' in config:
        config.set("DEFAULT", 'overlap factor', '0.15')
    with open('setting.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)

file_encoding = config['DEFAULT']['dvcfg encoding']
dvcfg_filename = 'voice.dvcfg'
oto_filename = 'oto.ini'
if config['DEFAULT']['backup existing oto'] == 'yes':
  oto_make_backup = True
elif config['DEFAULT']['backup existing oto'] == 'no':
  oto_make_backup = False
else:
  config.set("DEFAULT", 'backup existing oto', 'yes')
  oto_make_backup = True

overlap_factor = float(config['DEFAULT']['overlap factor'])
oto_encoding = config['DEFAULT']['oto encoding']

try:
  with open('dict.txt', 'x') as f:
    f.write('''n2 = n
a = あ
i = い
u = う
e = え
o = お
n = ん
ba = ば
bya = びゃ
cha = ちゃ
da = だ
dya = ぢゃ
fa = ふぁ
fya = ふゃ
ga = が
gya = ぎゃ
ha = は
hya = ひゃ
ja = じゃ
ka = か
qa = くぁ
kya = きゃ
ma = ま
mya = みゃ
na = な
nya = にゃ
pa = ぱ
pya = ぴゃ
ra = ら
rya = りゃ
sa = さ
sha = しゃ
ta = た
tsa = つぁ
tya = てゃ
va = ヴぁ
wa = わ
za = ざ
bi = び
chi = ち
di = でぃ
fi = ふぃ
gi = ぎ
hi = ひ
ji = じ
ki = き
mi = み
ni = に
pi = ぴ
ri = り
shi = し
ti = てぃ
tsi = つぃ
vi = ヴぃ
wi = うぃ
bu = ぶ
byu = びゅ
chu = ちゅ
du = づ
dyu = ぢゅ
fu = ふ
fyu = ふゅ
gu = ぐ
gyu = ぎゅ
hyu = ひゅ
ju = じゅ
ku = く
kyu = きゅ
mu = む
myu = みゅ
nu = ぬ
nyu = にゅ
pu = ぷ
pyu = ぴゅ
ru = る
ryu = りゅ
su = す
shu = しゅ
tu = てぅ
tsu = つ
tyu = ちゅ
vu = ヴぁ
vyu = ヴゅ
zu = ず
ngu = グ
be = べ
bye = びぇ
che = ちぇ
de = で
dye = ぢぇ
fye = ふぇ
fe = フェ
ge = げ
gye = ぎぇ
he = へ
hye = ひぇ
je = じぇ
ke = け
qe = くぇ
kye = きぇ
me = め
mye = みぇ
ne = ね
nye = にぇ
pe = ぺ
pye = ぴぇ
re = れ
rye = りぇ
se = せ
she = しぇ
te = て
tse = つぇ
tye = てぇ
ve = ヴぇ
we = うぇ
ze = ぜ
nge = ゲ
bo = ぼ
byo = びょ
cho = ちょ
do = ど
dyo = ぢょ
fo = ふぉ
fyo = ふょ
go = ご
gyo = ぎょ
ho = ほ
hyo = ひょ
jo = じょ
ko = こ
qo = くぉ
kyo = きょ
mo = も
myo = みょ
no = の
nyo = にょ
po = ぽ
pyo = ぴょ
ro = ろ
ryo = りょ
so = そ
sho = しょ
to = と
tso = つぉ
tyo = てょ
vo = ヴぉ
vyo = ヴょ
wo = を
ya = や
yu = ゆ
ye = いぇ
yo = よ
zo = ぞ
ngo = ゴ
zwa = ずぁ
zwi = ずぃ
zwe = ずぇ
zwo = ずぉ
wo = うぉ
wi = うぃ
si = すぃ''')
except:
  pass


def sec2mili(sec) -> int:
  return int(round(sec * 1000))

def to_alias(symbol: str, dict_path: str) -> str:
    '''change symbol based by dict.txt'''
    if symbol.startswith('-'):
        to_replace = symbol.split('-')[1].strip()
        is_first_cv = True
        is_vx = False
        is_last_cv = False
    elif '_' in symbol:
        to_replace = symbol.split('_')[1].strip()
        vowel = symbol.split('_')[0].strip()
        is_vx = True
        is_first_cv = False
        is_last_cv = False
    else:
        to_replace = symbol.strip()
        is_last_cv = True
        is_vx = False
        is_first_cv = False

    with open(dict_path, 'r') as f:
        dict_lines = f.readlines()

    status = 0
    for dict_line in dict_lines:
        if to_replace == dict_line.split('=')[0].strip():
            replaced = dict_line.split('=')[1].strip()
            status = 1
    if status == 0:
        replaced = to_replace

    if is_first_cv:
        result = f'- {replaced}'
    elif is_last_cv:
        result = replaced
    elif is_vx:
        result = f'{vowel} {replaced}'
    return result

form_class = uic.loadUiType("interface.ui")[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('icon.ico'))
        self.select_folder.clicked.connect(self._select_folder)
        self.run_convert.clicked.connect(self.dvcfg2oto)
        self.initUi()

    def initUi(self):
        self.run_convert.setDisabled(True)
        self.show_progress.clear()
        self.run_convert.setText('Convert')
      
      
    def show_message(self, content: str) -> None:
        self.show_progress.append(f' {content}')
        self.show_progress.append('')

    def _select_folder(self):
        global dir_path
        self.initUi()

        dir_path = Path(QFileDialog.getExistingDirectory(self, 'Select folder with ".dvcfg" and ".wav"s.'))
        self.show_path.setText(str(dir_path))
        check_path = dir_path / dvcfg_filename
        if check_path.is_file():
          self.show_message("...Found voice.dvcfg successfully. Click 'Convert' to start...")
          self.run_convert.setEnabled(True)
        else:
          self.show_message("...Can't find voice.dvcfg in this folder. Plz select correct one...")
  # Functionality
    def dvcfg2oto(self):
      to_ignore = []
      # load dvcfg
      fp = dir_path / dvcfg_filename

      with open_(fp) as fh:
        dvcfg = json.load(fh)
      self.show_message(f'[found] {len(dvcfg)} config items from {fp}')

      # parse dvcfg to oto
      dur = {}
      oto = []
      message_list = []
      for c in dvcfg.values():
        pitch = c['pitch']
        #if c['srcType'] != 'CV' and c['srcType'] != 'VX': continue
        
        symbol = c['symbol']

        wavName = c['wavName']
        if wavName not in dur:
          try:
            dur[wavName] = get_duration(str(fp.parent / wavName))
          except(FileNotFoundError):
            message_list.append(f'[Error] cannot load {wavName} for "{symbol}"\n>> ignored {wavName}')
            to_ignore.append(wavName)
          except Exception as e:
            message_list.append(f'[Error] cannot load {wavName} for "{symbol}"\n>> {e!r}')
            continue

        if wavName not in to_ignore:
          try:
            offset = sec2mili(c['startTime'] + c['connectPoint'])
          except:
            offset = sec2mili(c['startTime'] + c['startPoint'])

          try:
            consonant = sec2mili(c['vowelStart'] - c['connectPoint'])
          except:
            try:
              consonant = sec2mili(c['tailPoint'] - c['connectPoint'])
            except:
              consonant = overlap_factor * sec2mili(c['endPoint'] - c['startPoint'])

          try:
            preutterance = sec2mili(c['preutterance'] - c['connectPoint'])
          except:
            preutterance = consonant

          overlap = int(overlap_factor * preutterance)
          try:
            blank = sec2mili(dur[wavName] - c['startTime'] - c['vowelEnd'])
          except:
            try:
              blank = sec2mili(dur[wavName] - c['startTime'] - c['tailPoint']) - consonant + overlap
            except:
              blank = sec2mili(dur[wavName] - c['endPoint'] - c['startPoint']) - consonant * 4 - preutterance
          symbol = to_alias(c['symbol'], 'dict.txt')
          oto.append([wavName, f'{symbol}{pitch}', offset, consonant, blank, preutterance, overlap])
      
      self.show_message('\n'.join(message_list))
      # write oto
      oto_fp = fp.parent / oto_filename
      if oto_fp.is_file() and oto_make_backup:
        oto_bak_fp = Path(str(oto_fp).replace('.ini', '_original.ini'))
        shutil.move(oto_fp, oto_bak_fp)
        self.show_message(f'[oto-backup] oto.ini exists currently. \nChanged {oto_fp!s} to \n {oto_bak_fp!s}')
      else:
        pass
      with open(oto_fp, 'w', encoding=oto_encoding, errors='ignore') as fh:
        for o in sorted(oto):
          fh.write(f'{o[0]}={o[1]},{o[2]},{o[3]},{o[4]},{o[5]},{o[6]}\n')
      self.show_message(f"[Done] {len(oto)} config items\n >>> saved to {(fp.parent / oto_filename)!s}")
      self.run_convert.setText('Successed')
      self.run_convert.setDisabled(True)

def main():
    app = QApplication(sys.argv)
    main_window = WindowClass()
    
    main_window.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
    os.system('pause')