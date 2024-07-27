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
compound = pcq.compound(241)
print(compound)
