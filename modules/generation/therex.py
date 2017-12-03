#!/usr/bin/env python
__author__ = "Khalid Alnajjar"

'''
A class for accessing Thesaurus Rex (v2) API

Requirements: requests xmltodict (installable thourgh pip)
'''
import requests, urllib.parse, time, xmltodict, json

class TheRex:
    def __init__(self):
        self.base_url = 'http://ngrams.ucd.ie/therex2/common-nouns/'
        self.throttle = 2 # seconds
        self.last_query = None

    def map_item(self, r):
        return tuple([r['#text'], int(r['@weight'])])

    def member(self, concept):
        '''To obtain properties and categories of a given concept'''
        concept = urllib.parse.quote_plus(concept)
        url = '{0}common-nouns/member.action?member={concept}&kw={concept}&needDisamb=true&xml=true'.format(self.base_url, concept=concept)
        result = self._query_and_parse(url)
        return self._result_to_dict(result, 'MemberData')

    def modifier(self, modi, concept):
        '''To find cateogires of the input concept that share the input modifier(property)'''
        modi = urllib.parse.quote_plus(modi)
        concept = urllib.parse.quote_plus(concept)
        url = '{0}modifier.action?modi={modi}&ref={ref}&xml=true'.format(self.base_url, modi=modi, ref=concept)
        result = self._query_and_parse(url)
        return self._result_to_dict(result, 'ModifierData')

    def head(self, head, concept):
        '''To find properties of the input concept that are shared with the input head(category)'''
        head = urllib.parse.quote_plus(head)
        concept = urllib.parse.quote_plus(concept)
        url = '{0}head.action?head={head}&ref={ref}&xml=true'.format(self.base_url, head=head, ref=concept)
        result = self._query_and_parse(url)
        return self._result_to_dict(result, 'HeadData')

    def category(self, modi, cat):
        '''To find concepts that have a given modi(property) and also fall under a given category'''
        url = '{0}category.action?cate={1}&kw={2}&search=true&xml=true'.format(self.base_url, modi + ':' + cat, modi + '+' + cat)
        result = self._query_and_parse(url)
        return self._result_to_dict(result, 'CategoryData')

    def _query_and_parse(self, url):
        t = time.time()
        response = requests.get(url)
        time.sleep(max(self.throttle-(time.time()-t), 0)) # simple throttling
        return xmltodict.parse(response.content)

    def _result_to_dict(self, query_result, root_name):
        _root_content = query_result[root_name]
        result = {}
        if 'Categories' in _root_content and  'Category' in _root_content['Categories']:
            categories = map(lambda r: self.map_item(r), _root_content['Categories']['Category'])
            result['categories'] = dict(categories)
        if 'Members' in _root_content and 'Member' in _root_content['Members']:
            members = map(lambda r: self.map_item(r), _root_content['Members']['Member'])
            result['members'] = dict(members)
        if 'Modifiers' in _root_content and 'Modifier' in _root_content['Modifiers']:
            modifiers = map(lambda r: self.map_item(r), _root_content['Modifiers']['Modifier'])
            result['modifiers'] = dict(modifiers)
        if 'CategoryHeads' in _root_content and  'CategoryHead' in _root_content['CategoryHeads']:
            category_heads = map(lambda r: self.map_item(r), _root_content['CategoryHeads']['CategoryHead'])
            result['category_heads'] = dict(category_heads)
        return result

if __name__ == '__main__':
    tr = TheRex()
    target_concept = 'cat'
    print(json.dumps(tr.member(target_concept), indent=4))
    print()
    print(json.dumps(tr.modifier(modi='furry', concept=target_concept), indent=4))
    print()
    print(json.dumps(tr.head(head='mammal', concept=target_concept), indent=4))
    print()
    print(json.dumps(tr.category('furry', 'animal'), indent=4))
