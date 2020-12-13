let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Documents/Work/Research/New\ Paper/GSP_energy_disaggregator
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +20 gsp_disaggregator.py
badd +590 gsp_support.py
badd +1 term://.//19266:/bin/bash
badd +19 realtime_disaggregator.py
badd +189 ../disaggregation.py
badd +1 house_2_output_disaggr.csv
badd +0 term://.//29845:/bin/bash
badd +7213 output_aggr.csv
badd +21 dataset_visualize.py
badd +0 term://.//7662:/bin/bash
badd +0 createdataset.py
argglobal
silent! argdel *
$argadd gsp_disaggregator.py
set stal=2
edit gsp_support.py
set splitbelow splitright
wincmd _ | wincmd |
split
1wincmd k
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe '1resize ' . ((&lines * 62 + 41) / 82)
exe 'vert 1resize ' . ((&columns * 159 + 159) / 318)
exe '2resize ' . ((&lines * 62 + 41) / 82)
exe 'vert 2resize ' . ((&columns * 158 + 159) / 318)
exe '3resize ' . ((&lines * 16 + 41) / 82)
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 593 - ((19 * winheight(0) + 31) / 62)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
593
normal! 067|
wincmd w
argglobal
if bufexists('realtime_disaggregator.py') | buffer realtime_disaggregator.py | else | edit realtime_disaggregator.py | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 54 - ((34 * winheight(0) + 31) / 62)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
54
normal! 018|
wincmd w
argglobal
if bufexists('term://.//19266:/bin/bash') | buffer term://.//19266:/bin/bash | else | edit term://.//19266:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 3577 - ((15 * winheight(0) + 8) / 16)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3577
normal! 075|
wincmd w
exe '1resize ' . ((&lines * 62 + 41) / 82)
exe 'vert 1resize ' . ((&columns * 159 + 159) / 318)
exe '2resize ' . ((&lines * 62 + 41) / 82)
exe 'vert 2resize ' . ((&columns * 158 + 159) / 318)
exe '3resize ' . ((&lines * 16 + 41) / 82)
tabedit createdataset.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd _ | wincmd |
split
1wincmd k
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe 'vert 1resize ' . ((&columns * 159 + 159) / 318)
exe '2resize ' . ((&lines * 39 + 41) / 82)
exe 'vert 2resize ' . ((&columns * 158 + 159) / 318)
exe '3resize ' . ((&lines * 39 + 41) / 82)
exe 'vert 3resize ' . ((&columns * 158 + 159) / 318)
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 64 - ((63 * winheight(0) + 39) / 79)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
64
normal! 027|
wincmd w
argglobal
if bufexists('dataset_visualize.py') | buffer dataset_visualize.py | else | edit dataset_visualize.py | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 25 - ((16 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
25
normal! 033|
wincmd w
argglobal
if bufexists('term://.//7662:/bin/bash') | buffer term://.//7662:/bin/bash | else | edit term://.//7662:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 162 - ((38 * winheight(0) + 19) / 39)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
162
normal! 076|
wincmd w
exe 'vert 1resize ' . ((&columns * 159 + 159) / 318)
exe '2resize ' . ((&lines * 39 + 41) / 82)
exe 'vert 2resize ' . ((&columns * 158 + 159) / 318)
exe '3resize ' . ((&lines * 39 + 41) / 82)
exe 'vert 3resize ' . ((&columns * 158 + 159) / 318)
tabedit gsp_disaggregator.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe '1resize ' . ((&lines * 60 + 41) / 82)
exe 'vert 1resize ' . ((&columns * 159 + 159) / 318)
exe '2resize ' . ((&lines * 18 + 41) / 82)
exe 'vert 2resize ' . ((&columns * 159 + 159) / 318)
exe 'vert 3resize ' . ((&columns * 158 + 159) / 318)
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 74 - ((49 * winheight(0) + 30) / 60)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
74
normal! 037|
wincmd w
argglobal
if bufexists('term://.//29845:/bin/bash') | buffer term://.//29845:/bin/bash | else | edit term://.//29845:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 875 - ((17 * winheight(0) + 9) / 18)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
875
normal! 075|
wincmd w
argglobal
if bufexists('realtime_disaggregator.py') | buffer realtime_disaggregator.py | else | edit realtime_disaggregator.py | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 52 - ((51 * winheight(0) + 39) / 79)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
52
normal! 010|
wincmd w
exe '1resize ' . ((&lines * 60 + 41) / 82)
exe 'vert 1resize ' . ((&columns * 159 + 159) / 318)
exe '2resize ' . ((&lines * 18 + 41) / 82)
exe 'vert 2resize ' . ((&columns * 159 + 159) / 318)
exe 'vert 3resize ' . ((&columns * 158 + 159) / 318)
tabnext 2
set stal=1
if exists('s:wipebuf') && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 winminheight=1 winminwidth=1 shortmess=filnxtToOF
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
