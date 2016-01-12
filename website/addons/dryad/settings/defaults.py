# DRYAD OAI-PMH metadata harvesting settings
# Note where needed, format as (date, prefix, dataset)
# At the moment, this part of the API is unused as the DataOne connection
# provides more information
DRYAD_OAI_IDENTIFY = "http://www.datadryad.org/oai/request?verb=Identify"
DRYAD_OAI_LISTSET = "http://www.datadryad.org/oai/request?verb=ListSets"
DRYAD_OAI_LISTMETADATAFORMAT = "http://www.datadryad.org/oai/request?verb=ListMetadataFormats"
DRYAD_OAI_LISTIDENTIFIERS = "http://www.datadryad.org/oai/request?verb=ListIdentifiers&from={}&metadataPrefix={}&set={}"
DRYAD_OAI_LISTRECORDS = "http://www.datadryad.org/oai/request?verb=ListRecords&from={}&metadataPrefix={}&set={}"
DRYAD_OAI_GETRECORD = "www.datadryad.org/oai/request?verb=GetRecord&identifier={}&metadataPrefix={}"
DRYAD_OAI_RESUMPTION = "http://www.datadryad.org/oai/request?verb=ListRecords&resumptionToken={}"

#Dataone API
DRYAD_DATAONE_LIST = "http://www.datadryad.org/mn/object"
DRYAD_DATAONE_METADATA = "https://datadryad.org/mn/object/{}"
DRYAD_DATAONE_DOWNLOAD = "https://datadryad.org/mn/object/{}/bitstream"
DRYAD_FILE_METADATA = "http://www.datadryad.org/mn/meta/{}/bitstream"

#SOLR Search Query
DRYAD_SOLR_SEARCH = "http://datadryad.org/solr/search/select/"

#Dryad Web API
DRYAD_WEB_API="http://datadryad.org/resource/{}"
