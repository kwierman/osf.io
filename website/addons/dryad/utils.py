import re # For parsing out file names
import requests
import xml.dom.minidom
import xml.etree.ElementTree as ET
from website.addons.dryad import settings as dryad_settings


class DryadConnection:
    """
        DryadConnection is a proxy class for connecting to the Dryad API.

        note: This will be expanded in the v2 API.

        A proxy class was needed for unit testing so that the connection object
        in each of the methods in this module can be replaced with a non-http
        using connection.
    """

    def get(self, url='localhost', params={}):
        if params:
            r = requests.get(url, params=params)
        else:
            r = requests.get(url)
        return r

    def post(self, url):
        r = requests.post(url)
        return r


class DryadRepository:
    def __init__(self, connection=DryadConnection()):
        self.connection = connection

    def get_dryad_metadata(self, doi="doi:10.5061/dryad.1850"):
        """ Retrieves the metadata of a dryad item in the form of xml.dom.minidom element
        :param doi: Dryad DOI in the form of "doi:10.5061/dryad.XXXX"
        :type doi: string
        :returns:  xml.dom.minidom.Document -- xml form of the dryad metadata
        :raises: urllib.error.HTTPError
        """
        resp = self.connection.get( dryad_settings.DRYAD_DATAONE_METADATA.format(doi) )
        # The below encoding is mandatory
        return xml.dom.minidom.parseString(resp.text.encode('utf-8'))

    def extract_dryad_title(self, metadata):
        return metadata.getElementsByTagName("dcterms:title")[0].firstChild.wholeText

    def get_dryad_title(self, doi="doi:10.5061/dryad.1850" ):
        metadata = self.get_dryad_metadata(doi)
        return self.extract_dryad_title(metadata)

    def check_dryad_doi(self, doi="doi:10.5061/dryad.1850"):
        """ Checks dryad dois for validity.
        Attempts to download data from
        :param doi: Dryad DOI in the form of "doi:10.5061/dryad.XXXX"
        :type doi: string
        :returns:  bool -- True if the doi is found in the dryad archive.
        :raises: urllib.error.HTTPError
        """
        resp = self.connection.get( dryad_settings.DRYAD_DATAONE_METADATA.format(doi) )
        if resp.status_code == 404:
            return False
        return True

    def list_dryad_dois(self, start_n=0, count=20):
        """ Retrieves list of Dryad packages from Dryad DataOne API.
        :param start_n: The first index of a package to be listed
        :type start_n: int
        :param count: The number of packages to be listed
        :type start_n: int
        :returns:  xml.dom.minidom.Document -- document of packages listed
        :raises: urllib.error.HTTPError
        """
        resp = self.connection.get( url=dryad_settings.DRYAD_DATAONE_LIST,
            params={'start': start_n,
                    'count': count,
                    'formatId':'http://www.openarchives.org/ore/terms' } )
        return xml.dom.minidom.parseString(resp.text)

    def file_metadata(self, doi='doi:10.5061/dryad.1850/1'):
        """ Retrieves file-specific metadata for a given file doi
        :param doi: The file of whose metadata is be retrieved
        :type doi: string
        :returns:  xml.dom.minidom.Document -- document of packages listed
        :raises: urllib.error.HTTPError
        """
        resp = self.connection.get( dryad_settings.DRYAD_FILE_METADATA.format(doi) )
        return xml.dom.minidom.parseString(resp.text)

    def download_dryad_file(self, doi="doi:10.5061/dryad.1850/1"):
        """ Returns a bitstream formatted document for a given file doi
        :param doi: The file to be downloaded
        :type doi: string
        :returns:  string -- file buffer
        :raises: urllib.error.HTTPError
        """
        return self.connection.get( dryad_settings.DRYAD_DATAONE_DOWNLOAD.format(doi) )

    def get_file_name(self, doi='doi:10.5061/dryad.1850/1'):
        """ Returns a bitstream formatted document for a given file doi
        :param doi: The file to be downloaded
        :type start_n: string
        :returns:  string -- file buffer
        :raises: urllib.error.HTTPError
        """
        resp = self.download_dryad_file(doi, connection)
        disposition = resp.headers['content-disposition']
        # The below calls strip in order to deal with inconsistency with quotations
        fname = re.findall('filename=(.+)', disposition)[0].strip('"')
        return fname

    def get_dryad_metadata_as_json(self,doi="doi:10.5061/dryad.1850"):
        metadata_xml = self.get_dryad_metadata(doi)

        #required by metadata standard
        ident = metadata_xml.getElementsByTagName("dcterms:identifier")[0].firstChild.wholeText
        title = metadata_xml.getElementsByTagName("dcterms:title")[0].firstChild.wholeText
        authors = [i.firstChild.wholeText for i in metadata_xml.getElementsByTagName("dcterms:creator")]

        #optional by metadata standard
        description = ""
        if len(metadata_xml.getElementsByTagName("dcterms:description"))>0:
            description = metadata_xml.getElementsByTagName("dcterms:description")[0].firstChild.wholeText
        date_submitted=""
        if len(metadata_xml.getElementsByTagName("dcterms:dateSubmitted"))>0:
            date_submitted = metadata_xml.getElementsByTagName("dcterms:dateSubmitted")[0].firstChild.wholeText
        date_available = ""
        if len(metadata_xml.getElementsByTagName("dcterms:available"))>0:
            date_available = metadata_xml.getElementsByTagName("dcterms:available")[0].firstChild.wholeText

        #Also optional, but treated as empty list
        subject = [i.firstChild.wholeText for i in metadata_xml.getElementsByTagName("dcterms:subject")]
        scientific_names = [i.firstChild.wholeText for i in metadata_xml.getElementsByTagName("dwc:scientificName")]
        temporal_info = [i.firstChild.wholeText for i in metadata_xml.getElementsByTagName("dcterms:temporal")]
        references = [i.firstChild.wholeText for i in metadata_xml.getElementsByTagName("dcterms:references")]
        files = [i.firstChild.wholeText for i in metadata_xml.getElementsByTagName("dcterms:hasPart")]
        return {'doi': doi,
                'ident': ident,
                'title': title,
                'authors': authors,
                'date_submitted': date_submitted,
                'date_available': date_available,
                'description': description,
                'subjects': subject,
                'scientific_names': scientific_names,
                'temporal_info': temporal_info,
                'references': references,
                'files': files}

    def get_package_list_as_json(self, start_n=0, count=20):
        """ Returns  a list of dryad packages formatted for knockout rendering
        :param start_n: The first index of a package to be listed
        :type start_n: int
        :param count: The number of packages to be listed
        :type start_n: int
        :returns:  dict -- Formatted list of dryad packages
        :raises: urllib.error.HTTPError
        """
        xml_list = self.list_dryad_dois(start_n, count)

        count = int(xml_list.getElementsByTagName("d1:objectList")[0].attributes["count"].value)
        start = int(xml_list.getElementsByTagName("d1:objectList")[0].attributes["start"].value)
        total = int(xml_list.getElementsByTagName("d1:objectList")[0].attributes["total"].value)

        ret = {"end": start + count,
                "start": start,
                "total": total,
                "package_list": []}

        for package in xml_list.getElementsByTagName("objectInfo"):
            ident = package.getElementsByTagName("identifier")[0].firstChild.wholeText
            doi = "doi:" + ident.split("dx.doi.org/")[1].split("?")[0]
            ret['package_list'].append(self.get_dryad_metadata_as_json(doi))
        return ret

    def get_dryad_search_results(self, start_n=0, count=20, query=''):
        """ Returns  a list of dryad packages formatted for knockout rendering by search string
        Dryad content can be searched using a SOLR interface.
        Basic query: http://datadryad.org/solr/search/select/?q=Galliard
        Field-specific query: http://datadryad.org/solr/search/select/?q=dwc.ScientificName:drosophila
        Search all text for a string, but limits results to two specified fields:
        http://datadryad.org/solr/search/select/?q=Galliard&fl=dc.title,dc.contributor.author
        Dryad data based on an article DOI:
        http://datadryad.org/solr/search/select/?q=dc.relation.isreferencedby:10.1038/nature04863&fl=dc.identifier,dc.title_ac
        All terms in the dc.subject facet, along with their frequencies:
        http://datadryad.org/solr/search/select/?q=location:l2&facet=true&facet.field=dc.subject_filter&facet.minCount=1&facet.limit=5000&fl=nothing
        Article DOIs associated with all data published in Dryad over the past 90 days:
        http://datadryad.org/solr/search/select/?q=dc.date.available_dt:%5BNOW-90DAY/DAY%20TO%20NOW%5D&fl=dc.relation.isreferencedby&rows=1000000
        Data DOIs published in Dryad during January 2011, with results returned in JSON format:
        http://datadryad.org/solr/search/select/?q=location:l2+dc.date.available_dt:%5B2011-01-01T00:00:00Z%20TO%202011-01-31T23:59:59Z%5D&fl=dc.identifier&rows=1000000&wt=json
        For more about using SOLR, see the Apache SOLR documentation.
        :param start_n: The first index of a package to be listed
        :type start_n: int
        :param count: The number of packages to be listed
        :type start_n: int
        :returns:  dict -- Formatted list of dryad packages
        :raises: urllib.error.HTTPError
        """
        #quote = urllib.quote(query.encode('ascii'), safe='')
        resp = self.connection.get(url=dryad_settings.DRYAD_SOLR_SEARCH,
            params={'q':query,
                'archived': 'True',
                 'formatId':'http://www.openarchives.org/ore/terms',
                 'start': start_n,
                 'count': count,
                 'fq':'location.coll:2'})
        x = xml.dom.minidom.parseString(resp.text.encode('utf-8'))
        return x

    def get_dryad_search_results_json_formatted(self, start_n=0, count=10, query="Phylogenetic"):
        """ Returns  a list of dryad packages formatted for knockout rendering
        :param start_n: The first index of a package to be listed
        :type start_n: int
        :param count: The number of packages to be listed
        :type start_n: int
        :returns:  dict -- Formatted list of dryad packages
        :raises: urllib.error.HTTPError
        """
        xml_list = self.get_dryad_search_results(start_n, count, query)
        #now here is the list of results....

        count = int(xml_list.getElementsByTagName("result")[0].attributes["numFound"].value)
        start = int(xml_list.getElementsByTagName("result")[0].attributes["start"].value)
        total = int(xml_list.getElementsByTagName("result")[0].attributes["numFound"].value)

        ret = {"end": start + count,
                "start": start,
                "total": total,
                "package_list": []}

        for doc in xml_list.getElementsByTagName("doc"):
            identifier = [i.firstChild.firstChild.wholeText for i in doc.getElementsByTagName("arr") if i.hasAttribute("name") and i.getAttribute("name") == "dc.identifier"]
            if len(identifier)==0:
                identifier=""
                continue
            else:
                identifier = identifier[0]
            if 'doi' in identifier:
                doi = identifier
                ret['package_list'].append(self.get_dryad_metadata_as_json(doi))
            else:
                ret['package_list'].append({})
        return ret
