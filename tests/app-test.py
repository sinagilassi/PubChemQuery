import pubchemquery as pcq

# get a cid by name
# cid = pcq.get_cid_by_name('benzene')
# print(cid)

# get all cids by name
# cids = pcq.get_cids_by_name('benzene')
# print(cids)

# get 2d image
# image = pcq.get_2d_image_by_cid(241)
# print(image)

# make a compound
cid = 2244
# compound = pcq.compound(cid)
# name
name = '2-acetyloxybenzoic acid'
compound = pcq.compound(name=name)
print(compound)
# properties
print(compound.InChI)
print(compound.InChIKey)
print(compound.IUPACName)
