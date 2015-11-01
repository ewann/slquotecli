import SoftLayer
    #needed to interact with SL api

def conn_obj():
    client = SoftLayer.create_client_from_env(timeout=240)
    return client

def list_all_quotes(client):
    return client['Account'].getQuotes()

def download_quote_pdf(client, quoteID):
    #because: logic!? Anyway... this works
    return client['Billing_Order_Quote'].getPdf(id=quoteID)

def list_all_products(client):
    categoryObjectMask = "mask[id, name]"
    return client['Product_Package'].getAllObjects(mask=categoryObjectMask)

def get_existing_quote_container(client, quoteID):
    container = client['Billing_Order_Quote'].getRecalculatedOrderContainer( \
        id=quoteID)
    return container #['orderContainers'][0]

def verify_quote_or_order(client, container):
    return client['Product_Order'].verifyOrder(container)

def place_quote(client, container):
    return client['Product_Order'].placeQuote(container)
    #same approach can be used wih an existing quote id, as well as a quote container?
#result = client['Billing_Order_Quote'].verifyOrder(orderQuoteId)

    #this can be used to enumberate all orders in the account
#pp.pprint(client['Billing_Order'].getAllObjects())
