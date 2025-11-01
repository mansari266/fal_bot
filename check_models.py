import google.generativeai as genai

genai.configure(api_key="AIzaSyBy8FiqRNsfgKHBkUu-mFKgNV_aSWdy4e4")

for model in genai.list_models():
    print(model.name)
