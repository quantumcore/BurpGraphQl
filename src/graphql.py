"""
Author: QuantumCore (fahad) quantumcore@protonmail.com
graphql.py (c) 2022
Desc: GraphQL Controller for Burpsuite Enterprise Server
"""

from python_graphql_client import GraphqlClient
from .query import *
import json
from colorama import Fore, Style

ok = Style.BRIGHT + "[" + Fore.GREEN + "+" + Style.RESET_ALL + Style.BRIGHT + "]" + Style.RESET_ALL
not_ok = Style.BRIGHT + "[" + Fore.RED + "-" + Style.RESET_ALL + Style.BRIGHT + "]" + Style.RESET_ALL

class BurpGraphQL:
    """
    Main Controller for Burpsuite Graphql
    Arguments :
    - BURP - The http://ip:port/graphql/v1 of your Burpsuite Server
    - AUTH - API authorization key.

    Methods :
    - run_query(Query) - Executes a query on the server and returns it's response
    - start_scan(SiteID, ConfigID) - Starts a Scan Immediatley
    - new_site(folderid, urls) - Create a new Site
    - SiteTree() - Returns all Sites
    - stop_scan(ID) - Stop a scan by ID
    - list_scans() - List all scans
    - scan_info(ID) - Get Scan information by id
    - get_report(ID) - Get Scan Report by ID
    - jsonresponse (msg) - Give a response message in json
    - get_folder_id(folder_name) - Get Folder ID by name
    - get_site_id(site_name) - Get Site ID by name
    - get_scan_id(site_name) - Get Scan ID by name
    - get_percentage(site_name) - Get Scan progress by name
    """
    burp_online = False
    def __init__(self, BURP, AUTH):
        self.BURP = BURP
        self.AUTH = AUTH

        try:
            self.headers = { "Authorization": self.AUTH}
            self.client = GraphqlClient(endpoint=self.BURP, headers=self.headers)

            # Testing the connection by executing a random (SITE_TREE) query on burpsuite
            try:
                test = self.client.execute(SITE_TREE)
                self.burp_online = True
                print(ok + " Burpsuite online.")
            except ConnectionRefusedError:
                print(not_ok + Fore.RED + Style.BRIGHT + " BURPGRAPHQL ERROR : " + Style.RESET_ALL + str(e))

            except Exception as e:
                print(not_ok + Fore.RED + Style.BRIGHT +" BURPGRAPHQL ERROR : " +  Style.RESET_ALL+  str(e))

        except Exception as e:
            print( not_ok + Fore.RED + Style.BRIGHT + " BURPGRAPHQL ERROR : " + Style.RESET_ALL+ str(e) )

    
    def jsonresponse(self, msg):
        response = {"message" : msg}
        return json.dumps(response, indent=4, sort_keys=True)


 

    # Run GraphQL Query and return it's response
    def run_query(self, Query):
        if(self.burp_online):
            try:
                response = self.client.execute(Query)
                return response # JSON
            except Exception as e:
                print(not_ok + " Error  : " + str(e))
        else:
            print(not_ok + " Error Burpsuite is not online/available.")

    def start_scan(self, SiteID, ConfigID):
        """
        Start a Scan
        """
        if(self.burp_online):
            try:
                Query_1 = START_SCAN.replace("{SITE_ID}", SiteID)
                Query = Query_1.replace("{CONFIG_ID}", ConfigID)
                rp = self.run_query(Query)
                return rp
            except Exception as e:
                print(not_ok + " Error  : " + str(e))
        else:
            print(not_ok + " Error Burpsuite is not online/available.")

    # This will not be used
    def get_configs(self):
        if(self.burp_online):
            try:
                Configs = self.run_query(GET_SCAN_CONFIGS)
                return Configs
            except Exception as e:
                print(not_ok + " Error  : " + str(e))
        else:
            print(not_ok + " Error Burpsuite is not online/available.")

    
    def new_site(self, site, parent_id):
        if(self.burp_online):
            try:
                Query = NEW_SITE.replace("{SITENAME}", site)
                Q = Query.replace("{PARENT_ID}", parent_id)
                f = self.run_query(Q)
                return f
            except Exception as e:
                print(not_ok + " Error  : " + str(e))
        else:
            print(not_ok + " Error Burpsuite is not online/available.")

    def SiteTree(self):
        if(self.burp_online):
            try:
                Query = self.run_query(SITE_TREE)
                return Query
            except Exception as e:
                print(not_ok + " Error  : " + str(e))
        else:
            print(not_ok + " Error Burpsuite is not online/available.")

    def stop_scan(self, ID):
        # Cancel a Scan
        if(self.burp_online):
            try:
                Query = CANCEL_SCAN.replace("{ID}", ID)
                Q = self.run_query(Query)
                return Q
            except Exception as e:
                print(not_ok + " Error  : " + str(e))
        else:
            print(not_ok + " Error Burpsuite is not online/available.")

    def get_folder_id(self, folder_name):
        if(self.burp_online):
            x = self.run_query(FOLDER_TREE)
            val = json.loads(json.dumps(x['data']['site_tree']))
            for x in val['folders']:
                if(x['name'] == folder_name):
                    return x['id']
        else:
            print(not_ok + " Error Burpsuite is not online/available.")

    def get_site_id(self, site_name):
        if(self.burp_online):
            tree = self.run_query(SITE_TREE)
            pval = json.dumps(tree['data']['site_tree']['sites'])
            val = json.loads(pval)
            for site in val:
                if(site['name'] == site_name):
                    return site['id']
        else:
            print(not_ok + " Error Burpsuite is not online/available.")

    def get_scan_id(self, site_name):
        if(self.burp_online):
            sc = json.loads(self.list_scans())
            for s in sc:
                scan = s['data']['scan']
                if(scan['site_name'] == site_name):
                    return scan['id']
        else:
            print(not_ok + " Error Burpsuite is not online/available.")

    def get_percentage(self, site_name):
        try:
            if(self.burp_online):
                scanID = self.get_scan_id(site_name)
                if(scanID is not None):
                    gp = GET_SCAN_METRICS.replace("{SCANID}", scanID)
                    Query = self.run_query(gp)
                    return Query['data']['scan']['scan_metrics']['crawl_and_audit_progress_percentage']
            else:
                print(not_ok + " Error Burpsuite is not online/available.")
        except Exception as e:
            print(not_ok + " Error getting scan percentage for " + site_name + " : " + str(e))

    def list_scans(self):
        """
        This function lists all Scans
        """
        if(self.burp_online):
            try:
                l = []
                data = self.run_query(GET_SCANS)
                scans = data['data']['scans']
                for x in scans:
                    scanid = x['id'].strip()
                    new_q = GET_SCAN.replace("{SCAN_ID}", scanid)
                    response = self.run_query(new_q)
                    l.append(response)
                return json.dumps(l, indent=4, sort_keys=True) 
            except Exception as e:
                print(not_ok + " Error  : " + str(e))
        else:
            print(not_ok + " Error Burpsuite is not online/available.")

    def scan_info(self, ID):
        """
        return Scan information by id
        """
        if(self.burp_online):
            try:
                q = GET_SCAN.replace("{SCAN_ID}", ID)
                response = self.run_query(q)
                print(q)
                return json.dumps(response, indent=4, sort_keys=True)
            except Exception as e:
                print(not_ok + " Error  : " + str(e))
        else:
            print(not_ok + " Error Burpsuite is not online/available.")

    
    def get_report(self, ID):
        if(self.burp_online):
            try:
                q = GET_REPORT.replace("{SCAN_ID}", ID)
                response = self.run_query(q)
                return response['data']['scan_report']['report_html']
            except Exception as e:
                print(not_ok + " Error  : " + str(e))
        else:
            print(not_ok + " Error Burpsuite is not online/available.")
        

    def create_folder(self, ID, NAME):
        if(self.burp_online):
            try:
                q = CREATE_FOLDER.replace("{PARENT_ID}", ID)
                final = q.replace("{NAME}", NAME)
                #print(final)
                response = self.run_query(final)

                if(not_ok + " Error s" in response):
                    print("[BURPGRAPHQL] Error creating folder : " + str(response))
                    emsg = response['errors'][0]['message']
                    return self.jsonresponse(emsg)
                else:
                    print("[BURPGRAPHQL] Created folder with ID : " + str(response['data']['create_folder']['folder']['id']))
                    return self.jsonresponse("Folder created successfully.")

            except Exception as e:
                print(not_ok + " Error  : " + str(e))
        else:
            print(not_ok + " Error Burpsuite is not online/available.")