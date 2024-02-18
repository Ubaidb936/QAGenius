## Set pdf path (Required)
pdfPath = "doc.pdf"
    ##examples
    ##pdfPath = "https://www.dobs.pa.gov/Documents/Publications/Brochures/The%20Basics%20for%20Investing%20in%20Stocks.pdf"
    ##pdfPath = "doc.pdf"



##Set hugginface token (Required)
hf_token = "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"
##examples
    ##pdfPath = "https://www.dobs.pa.gov/Documents/Publications/Brochures/The%20Basics%20for%20Investing%20in%20Stocks.pdf"
    ##pdfPath = "doc.pdf"




## Set huggingFace llm model id (Required)
model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"





##What the document is about (Required)
title = "understand the basics of the stock market"
    # examples
    # title = "understand the basics of the stock market"



##datasetName to push it into huggingface (Required)
datasetName = "stock_market_basics"
 ##examples
    ##datasetName = "stock_market_basics"
    ##Note: datasetName must use alphanumeric chars or '-', '_', '.', '--' and '..' are forbidden, '-' and '.' cannot start or end the name, max length is 96



##Some keywords in the doc separated by, (Optional)
keywordsRelatedToPdfDoc = None
    ##examples
    ##keywordsRelatedToPdfDoc = "stock, stop order, start order."
    



