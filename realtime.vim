let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Documents/Work/Research/New\ Paper/GSP_energy_disaggregator
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +70 gsp_disaggregator.py
badd +30 gsp_support.py
badd +0 term://.//9105:/bin/bash
badd +0 realtime_disaggregator.py
badd +189 ../disaggregation.py
argglobal
silent! argdel *
$argadd gsp_disaggregator.py
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
exe '1resize ' . ((&lines * 47 + 42) / 84)
exe 'vert 1resize ' . ((&columns * 159 + 159) / 318)
exe '2resize ' . ((&lines * 47 + 42) / 84)
exe 'vert 2resize ' . ((&columns * 158 + 159) / 318)
exe '3resize ' . ((&lines * 34 + 42) / 84)
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
let s:l = 47 - ((19 * winheight(0) + 23) / 47)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
47
normal! 037|
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
let s:l = 80 - ((32 * winheight(0) + 23) / 47)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
80
normal! 041|
wincmd w
argglobal
if bufexists('term://.//9105:/bin/bash') | buffer term://.//9105:/bin/bash | else | edit term://.//9105:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 3550 - ((15 * winheight(0) + 17) / 34)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
3550
normal! 04|
wincmd w
3wincmd w
exe '1resize ' . ((&lines * 47 + 42) / 84)
exe 'vert 1resize ' . ((&columns * 159 + 159) / 318)
exe '2resize ' . ((&lines * 47 + 42) / 84)
exe 'vert 2resize ' . ((&columns * 158 + 159) / 318)
exe '3resize ' . ((&lines * 34 + 42) / 84)
tabnext 1
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
