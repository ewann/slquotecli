
def main():
  print ("")
  print ("")
  print ("Press the number then <enter> for the option you want:")
  print ("")
  print ("  1 - Show all quotes in the account")
  print ("  2 - Download PDF for a specific quote")
  print ("  3 - List all SoftLayer_Product_Package(s)")
  print ("  4 - Re-verify existing quote")
  print ("  5 - Duplicate existing quote")
  print ("  6 - <BROKEN?> Create Order Cart")
  print ("  7 - List SoftLayer_Product_Package required options")
  print ("  8 - List DataCenter locations")
  print ("  9 - List DataCenter location groups")
  print ("  0 - Exit")
  user_input = raw_input("Your choice: ")
  return int(user_input)

def download_quote_pdf():
  print ("")
  print ("")
  print ("Enter the id for the quote you wish to download:")
  user_input = raw_input("id: ")
  return int(user_input)

def reverify_existing_quote():
  print ("")
  print ("")
  print ("Enter the id for the quote you wish to re-verify:")
  user_input = raw_input("id: ")
  return int(user_input)

def duplicate_existing_quote():
  print ("")
  print ("")
  print ("Enter the id for the existing quote you wish to duplicate:")
  user_input = raw_input("id: ")
  return int(user_input)

def create_order_cart():
  print ("")
  print ("")
  print ("Enter the id for the source quote you wish to cart-ify:")
  user_input = raw_input("id: ")
  return int(user_input)

def list_product_package_required_options():
  print ("")
  print ("")
  print ("Enter the SoftLayer_Product_Package id for which you")
  print ("would like to see the required options:")
  user_input = raw_input("id: ")
  return int(user_input)
