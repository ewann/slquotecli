import SoftLayer
    #needed to interact with SL api

def conn_obj():
    client = SoftLayer.create_client_from_env(timeout=240)
    return client

def all_quotes(client):
     return client['Account'].getQuotes()

def download_quote_pdf(client, quoteID):
    #because: logic!? Anyway... this works
    return client['Billing_Order_Quote'].getPdf(id=quoteID)

#pp.pprint(result)
