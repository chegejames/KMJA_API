import glob
from os import *
from pandas import *
import pandas as pd
from sys import *
import re

data_dict = {"ids_pfnos":np.nan, "pfnos":np.nan}

continue_to_next_step = True

def get_members_csv(member_list):
  if member_list in glob.glob(member_list):
    data = pd.read_csv(member_list)
    ids_count = data.id.count()
    use_data_response = raw_input("There are '%d' members in this list should I use it [Y/N]" %(ids_count))
      
    if re.match('^\s*[Y|y]\s*$', use_data_response): 
        process_members_list(data)
    else:
      exit()
  else:
    wrong_file_reply = raw_input("The file '%s' is not present, enter a new file or 'q' to quit: " %(member_list))
    if re.match('^\s*[Q|q]\s*$',wrong_file_reply): 
      exit()
    else:
      get_members_csv(wrong_file_reply.strip())


def get_payment_text(payment_list):
  if payment_list in glob.glob(payment_list):
    try:
      process_payment_list(payment_list)
    except:
      print("Error could parse the payment file '%s'" %(payment_list))
  else:
    wrong_file_reply = raw_input("The file '%s' in not present, enter a new file or 'q' to quit: " %(payment_list))
    if re.match('^[\s*[Q|q]\s*$', wrong_file_reply):
      exit()
    else:
      get_payment_text(wrong_file_reply.strip())

def process_members_list(data):
  global data_dict
  data_dict["ids_pfnos"] = data[["id", "pfno"]]

def process_payment_list(doc):
  data = parse_text_file(doc)
  global data_dict
  data_dict["pfnos"] = data[["pfno"]]


#IMPLEMENT
def parse_text_file(doc):
  return pd.read_csv(doc)

def generate_csv_with_ids():
  global data_dict
  try:
    ids_to_invoice = merge(data_dict["ids_pfnos"], data_dict["pfnos"], on="pfno")[["id"]]
  except:
    print("Error: could not merge the data sets")

  try:
    ids_to_invoice.to_csv("Todays_data.csv", index=False)
    print("Saved the data to file")
  except:
    print("Error: could not save the data")

def exit(): 
  global continue_to_next_step
  continue_to_next_step = False

def prompt_for_member_list():
  member_list = raw_input("Enter the file name for the members' list: ")
  get_members_csv(member_list.strip())


if __name__ == "__main__":

    prompt_for_member_list()

    if continue_to_next_step == True:
      payment_list = raw_input("Enter the file name for the payments: ")
      get_payment_text(payment_list.strip())
      generate_csv_with_ids()

