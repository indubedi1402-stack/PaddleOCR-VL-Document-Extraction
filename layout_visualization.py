from paddleocr import PPStructureV3

pipeline = PPStructureV3(enable_mkldnn=False)

output = pipeline.predict("samples/invoice.png")

for res in output:
    res.save_to_json("output/layout")
    res.save_to_img("output/layout")

print("Layout visualization completed successfully!")
