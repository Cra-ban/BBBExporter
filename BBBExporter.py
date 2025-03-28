from urllib.request import urlopen
import pdfkit

def splitString(strng, sep, pos):
    strng = strng.split(sep)
    return sep.join(strng[:pos]), sep.join(strng[pos:])

# unnecessary ASCII-Art
print(r"""
   ___  ___  ___      ____                    __         
  / _ )/ _ )/ _ )____/ __/_ __ ___  ___  ____/ /____ ____
 / _  / _  / _  /___/ _/ \ \ // _ \/ _ \/ __/ __/ -_) __/
/____/____/____/   /___//_\_\/ .__/\___/_/  \__/\__/_/   
                            /_/  (not endorsed by H.D. Lang)
""")


presentationURL = input("\nEnter the BBB presentation URL: ")
outputFilename = input("\nEnter the output file name (without extension):")

trimmedURL = presentationURL.strip()    # remove any whitespace

presentationID = splitString(presentationURL, "/", -1)[1]   ## split url at last "/"
domainName = splitString(presentationURL, "/", 3)[0]    # split url at second "/"

# links to the svg stuff
baseSvgURL = domainName + "/presentation/" + presentationID + "/"
svgURL = domainName + "/presentation/" + presentationID + "/shapes.svg"

page = urlopen(svgURL)  
svg_bytes = page.read()
svgData = svg_bytes.decode("utf-8")

# replacing some things with other things(or nothing)
svgDataMod = svgData
svgDataMod = svgDataMod.replace("<image", "<svg viewBox=\"0 0 1600 976\"> <image")
svgDataMod = svgDataMod.replace("presentation/", baseSvgURL+"/presentation/")
svgDataMod = svgDataMod.replace("visibility:hidden", "")
svgDataMod = svgDataMod.replace("<!DOCTYPE svg PUBLIC \"-//W3C//DTD SVG 1.1//EN\" \"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd\">", "")
svgDataMod = svgDataMod.replace("<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" id=\"svgfile\" style=\"position:absolute;height:600px;width:800px\" version=\"1.1\" viewBox=\"0 0 800 600\">","")
svgDataMod = svgDataMod.replace("display=\"none\"", "")

svgDataInitial = svgDataMod.split("<svg")[0]    # everything before the first svg tag

# data after the first svg tag
svgDataCombined = svgDataMod.split("<svg")[1:]  
svgDataCombined = "</svg> <svg".join(svgDataCombined)   

svgDataOut = "<html>\n<body>\n"+svgDataInitial+"<svg"+svgDataCombined+"\n</body>\n</html>"

# save as svg (Does not work)
# f = open((outputFilename+".svg"),"w")
# f.write(svgDataInitial+"<svg"+svgDataCombined)
# f.close()
# print("svg-file has been saved in the current directory as "+ outputFilename+".svg")

# save as html
f = open((outputFilename+".html"),"w")
f.write(svgDataOut)
f.close()
print("HTML-file has been saved in the current directory as "+ outputFilename+".html")

# save as pdf
pdfkit.from_string(svgDataOut, (outputFilename+".pdf"))
print("PDF has been saved in the current directory as "+ outputFilename+".pdf")
