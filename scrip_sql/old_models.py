from django.db import models

# Create your models here.


# Divisions file (division.dmp):
# 	division id				-- taxonomy database division id
# 	division cde				-- GenBank division code (three characters)
# 	division name				-- e.g. BCT, PLN, VRT, MAM, PRI...
# 	comments


class Division(models.Model):
    division_id = models.IntegerField(primary_key=True,auto_created=False)
    division_code = models.CharField(max_length=3)
    division_name = models.CharField(max_length=100)
    comments = models.CharField(blank=True,max_length=100)

# Genetic codes file (gencode.dmp):
# 	genetic code id				-- GenBank genetic code id
# 	abbreviation				-- genetic code name abbreviation
# 	name					-- genetic code name
# 	cde					-- translation table for this genetic code
# 	starts					-- start codons for this genetic code


class Gencode(models.Model):
    genetic_code_id = models.IntegerField(primary_key=True,auto_created=False)
    abbreviation = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=200,blank=True)
    starts = models.CharField(max_length=200,blank=True)

# fields:
# 	tax_id					-- node id in GenBank taxonomy database
#  	parent tax_id				-- parent node id in GenBank taxonomy database
#  	rank					-- rank of this node (superkingdom, kingdom, ...)
#  	embl code				-- locus-name prefix; not unique
#  	division id				-- see division.dmp file
#  	inherited div flag  (1 or 0)		-- 1 if node inherits division from parent
#  	genetic code id				-- see gencode.dmp file
#  	inherited GC  flag  (1 or 0)		-- 1 if node inherits genetic code from parent
#  	mitochondrial genetic code id		-- see gencode.dmp file
#  	inherited MGC flag  (1 or 0)		-- 1 if node inherits mitochondrial gencode from parent
#  	GenBank hidden flag (1 or 0)            -- 1 if name is suppressed in GenBank entry lineage
#  	hidden subtree root flag (1 or 0)       -- 1 if this subtree has no sequence data yet
#  	comments				-- free-text comments and citations

class Nodes(models.Model):
    tax_id = models.IntegerField(primary_key=True,verbose_name='id',auto_created=False) # 主键
    parent_tax_id =models.IntegerField(verbose_name='parent_id')
    rank = models.CharField(max_length=100,verbose_name='rank')
    embl_code = models.CharField(max_length=100)
    division_id = models.ForeignKey(Division,on_delete=models.CASCADE) # 关联division
    inherited_div_flag = models.BinaryField(default=0)
    genetic_code_id = models.ForeignKey(Gencode,on_delete=models.CASCADE) # 关联gencode
    inherited_GC_flag = models.BinaryField(default=0)
    mitochondrial_genetic_code_id = models.IntegerField() #关联gencode
    inherited_MGC_flag = models.BinaryField(default=0)
    GenBank_hidden_flag = models.BinaryField(default=0)
    hidden_subtree_root_flag = models.BinaryField(default=0)
    comments = models.CharField(blank=True,max_length=100)

# Taxonomy names file (names.dmp):
# 	tax_id					-- the id of node associated with this name
# 	name_txt				-- name itself
# 	unique name				-- the unique variant of this name if name not unique
# 	name class				-- (synonym, common name, ...)

class Name(models.Model):
    tax_id = models.ForeignKey(Nodes,on_delete=models.CASCADE)
    name_txt = models.CharField(max_length=100)
    # unique_name = models.CharField(unique=True,max_length=100)
    unique_name = models.CharField(max_length=100)
    name_class = models.CharField(max_length=100)


# Deleted nodes file (delnodes.dmp):
# 	tax_id					-- deleted node id

class DelNode(models.Model):
    tax_id = models.IntegerField()


# Merged nodes file (merged.dmp):
# 	old_tax_id                              -- id of nodes which has been merged
# 	new_tax_id                              -- id of nodes which is result of merging

class Merged(models.Model):
    old_tax_id = models.IntegerField()
    new_tax_id = models.IntegerField()

# Citations file (citations.dmp):
# 	cit_id					-- the unique id of citation
# 	cit_key					-- citation key
# 	pubmed_id				-- unique id in PubMed database (0 if not in PubMed)
# 	medline_id				-- unique id in MedLine database (0 if not in MedLine)
# 	url					-- URL associated with citation
# 	text					-- any text (usually article name and authors).
# 						-- The following characters are escaped in this text by a backslash:
# 						-- newline (appear as "\n"),
# 						-- tab character ("\t"),
# 						-- double quotes ('\"'),
# 						-- backslash character ("\\").
# 	taxid_list				-- list of node ids separated by a single space

class Citations(models.Model):
    cit_id = models.IntegerField(primary_key=True,verbose_name='id',auto_created=False)
    cit_key = models.CharField(blank=True,max_length=2000)
    pubmed_id = models.IntegerField(blank=True)
    medline_id = models.IntegerField(blank=True)
    url = models.CharField(max_length=2000,blank=True)
    text = models.CharField(max_length=2000,blank=True)
    taxid_list = models.CharField(max_length=2000,blank=True)
    # class Meta:
    #     unique_together = (
    #         ('pubmed_id','medline_id'),
    #         ('pubmed_id','cit_id'),
    #         ('medline_id','cit_id')
    #     )

