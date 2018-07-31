import local

iw = local.newText('iw')
iw.loadPlain('italian1-web.txt', 'iw', 'it')
iw=iw.segment()
fm = local.download('french')
ia=fm.align(iw)
ia.id='ia'
local.register(ia)
