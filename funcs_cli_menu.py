
def main():
  print ("")
  print ("")
  print ("Press the number then <enter> for the option you want:")
  print ("")
  print ("  1 - Show all quotes in the account")
  print ("  2 - Download PDF for a specific quote")
  print ("  3 - List all (Active) SoftLayer_Product_Package(s)")
  print ("  4 - Re-verify existing quote")
  print ("  5 - Duplicate existing quote")
  print ("  6 - <BROKEN?> Create Order Cart")
  print ("  7 - List SoftLayer_Product_Package required options for a given package")
  print (" 13 - List SoftLayer_Product_Package all options for a given package")
  print ("  8 - List Location_DataCenter (DC locations)")
  print ("  9 - List Location_Group(s)")
  print (" 10 - List Location_Group members")
  print (" 11 - List type of a Location_Group")
  print (" 12 - List Location_Group(s) location is member of")
  print ("  0 - Exit")
  user_input = raw_input("Your choice: ")
  try:
      return int(user_input)
  except:
      main()

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

def list_product_package_all_options():
  print ("")
  print ("")
  print ("Enter the SoftLayer_Product_Package id for which you")
  print ("would like to see all options:")
  user_input = raw_input("id: ")
  return int(user_input)

def get_location_group_members():
  print ("")
  print ("")
  print ("Enter the location id for which you")
  print ("would like to see its Location_Group membership:")
  user_input = raw_input("id: ")
  return int(user_input)

def get_location_group_type():
  print ("")
  print ("")
  print ("Enter the location id for which you")
  print ("would like to see its Location_Group type:")
  user_input = raw_input("id: ")
  return int(user_input)

def get_is_member_of_location_groups():
  print ("")
  print ("")
  print ("Enter the location id for which you")
  print ("would like to see its Location_Group membership:")
  user_input = raw_input("id: ")
  return int(user_input)
