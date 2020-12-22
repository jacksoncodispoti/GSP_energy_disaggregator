let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Documents/Work/Research/New\ Paper/GSP_energy_disaggregator
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +8 realtime_disaggregator.py
badd +2 dataset/house_2/config.config
badd +0 config.config
badd +0 term://.//10521:/bin/bash
argglobal
silent! argdel *
edit config.config
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd _ | wincmd |
split
wincmd _ | wincmd |
split
2wincmd k
wincmd w
wincmd w
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe '1resize ' . ((&lines * 23 + 44) / 88)
exe 'vert 1resize ' . ((&columns * 158 + 159) / 318)
exe '2resize ' . ((&lines * 13 + 44) / 88)
exe 'vert 2resize ' . ((&columns * 158 + 159) / 318)
exe '3resize ' . ((&lines * 48 + 44) / 88)
exe 'vert 3resize ' . ((&columns * 158 + 159) / 318)
exe 'vert 4resize ' . ((&columns * 159 + 159) / 318)
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
let s:l = 13 - ((9 * winheight(0) + 11) / 23)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
13
normal! 0
wincmd w
argglobal
if bufexists('dataset/house_2/config.config') | buffer dataset/house_2/config.config | else | edit dataset/house_2/config.config | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 2 - ((1 * winheight(0) + 6) / 13)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
2
normal! 0
wincmd w
argglobal
if bufexists('term://.//10521:/bin/bash') | buffer term://.//10521:/bin/bash | else | edit term://.//10521:/bin/bash | endif
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 27 - ((26 * winheight(0) + 24) / 48)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
27
normal! 078|
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
let s:l = 12 - ((11 * winheight(0) + 43) / 86)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
12
normal! 0
wincmd w
3wincmd w
exe '1resize ' . ((&lines * 23 + 44) / 88)
exe 'vert 1resize ' . ((&columns * 158 + 159) / 318)
exe '2resize ' . ((&lines * 13 + 44) / 88)
exe 'vert 2resize ' . ((&columns * 158 + 159) / 318)
exe '3resize ' . ((&lines * 48 + 44) / 88)
exe 'vert 3resize ' . ((&columns * 158 + 159) / 318)
exe 'vert 4resize ' . ((&columns * 159 + 159) / 318)
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
