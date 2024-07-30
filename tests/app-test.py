import pubchemquery as pcq

# get a cid by inchi
cid = pcq.get_cid_by_inchi(
    'InChI=1S/C6H5NO3/c8-6-3-1-5(2-4-6)7(9)10/h1-4,8H')
print(cid)

# get a cid by formula
# cid = pcq.get_cids_by_formula('C6H6')
# print(type(cid), len(cid))

# get a cid by name
# cid = pcq.get_cid_by_name('benzene')
# print(cid)

# get all cids by name
# cids = pcq.get_cids_by_name('benzene')
# print(type(cids), len(cids))

# get 2d image
# image = pcq.get_image_by_cid('241')
# print(image)

# image = pcq.get_image_by_name('benzene')
# print(image)

# get sdf by cid
# sdf = pcq.get_structure_by_cid('241')
# print(sdf)

# get sdf by name
# sdf = pcq.get_structure_by_name('benzene')
# print(sdf)

# get similar structure cids by cid
# cids = pcq.get_similar_structures_cids_by_compound_id('241')
# cids = pcq.get_similar_structures_cids_by_compound_id(
#     'C1=CC=CC=C1', compound_id='SMILES')
# cids = pcq.get_similar_structures_cids_by_compound_id(
#     'InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H', compound_id='InChI')
# print(type(cids), len(cids))


# make a compound
cid = 2244
# compound = pcq.compound(cid)
# name
name = '2-acetyloxybenzoic acid'
# compound = pcq.compound(name)
# print(compound)
# # properties
# # InChI
# print(compound.InChI)
# # InChIKey
# print(compound.InChIKey)
# # IUPACName
# print(compound.IUPACName)
# # image
# print(compound.image)
# # similar structure cids
# print(len(compound.similar_structure_cids))
# # dataframe
# print(compound.prop_df())
