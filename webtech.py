from flask_cors import CORS
import cv2
from flask import Flask, request, render_template, send_from_directory ,jsonify
import os
import numpy as np  
from keras.models import model_from_json
import time
import stat
flagg=False
app = Flask(__name__)
CORS(app)
json_file = open("C:\\Users\\anvitha poosarla\\Desktop\\webtech project\\model1.json", 'r')
file = os.stat ( "C:\\Users\\anvitha poosarla\\Desktop\\webtech project\\myfile.txt" )
original_time=time.ctime ( file[ stat.ST_MTIME ] )
loaded_model_json = json_file.read()
json_file.close()
prevline=""
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("C:\\Users\\anvitha poosarla\\Desktop\\webtech project\\model1.h5")
loaded_model._make_predict_function()
print("Loaded model from disk")

@app.route("/modification",methods=["GET"])
def mod():
	global prevline,original_time,flagg
	dictt=dict()
	flagg=False
	fileStatsObj = os.stat ( "C:\\Users\\anvitha poosarla\\Desktop\\webtech project\\myfile.txt" )
	modification_time = time.ctime ( fileStatsObj [ stat.ST_MTIME ] )
	print(modification_time,original_time)
	if(modification_time!=original_time):
		
		with open("C:\\Users\\anvitha poosarla\\Desktop\\webtech project\\myfile.txt", "r") as file:
			
			for line in file:
				print(line,flagg)
				line=line.strip("\n")
				if(flagg==True):
					val=line.split("|")
					dictt[val[0]]=val[1]
					
				if(prevline.strip("\n")==line.strip("\n")):
					flagg=True
				
			prevline=line
	print(dictt,prevline)
	original_time=modification_time	
	return jsonify(dictt),200	
	
@app.route("/original",methods=["GET"])
def orginal():
	global original_time ,prevline
	dictt=dict()
	fileStatsObj = os.stat ( "C:\\Users\\anvitha poosarla\\Desktop\\webtech project\\myfile.txt" )
	original_time = time.ctime ( fileStatsObj [ stat.ST_MTIME ] )
	with open("C:\\Users\\anvitha poosarla\\Desktop\\webtech project\\myfile.txt", "r") as file:
    
		for line in file:
			val=line.split("|")
			dictt[val[0]]=val[1]
		prevline=line
	print(original_time,prevline)	
	return jsonify(dictt),200
			


@app.route("/appy",methods=["POST"])
def apppy():
	sleep(60)
	return "yo"
@app.route("/rating",methods=["POST"])
def ratingg():
	print(request.data)
	#print(request)
	#for i in request.data:
	#	print(i)
	
	input=(request.data.decode("utf-8")) 
	print(input)
	input=input.split("|")
	username=input[0]
	rating=input[1]
	def append_new_line(text_to_append):

		with open("C:\\Users\\anvitha poosarla\\Desktop\\webtech project\\myfile.txt", "a+") as file_object:

			file_object.seek(0)

			data = file_object.read(100)
			if len(data) > 0:
				file_object.write("\n")

			file_object.write(text_to_append)
	#username="bla"
	#file1 = open("C:\\Users\\anvitha poosarla\\Desktop\\webtech project\\myfile.txt", "a")  # append mode 
	#file1.write(username+"|"+str(rating)) 
	#file1.close() 
	append_new_line(username+"|"+str(rating))
	return username,200




@app.route("/app",methods=["POST"])
def bla():
    X=[]
    path = os.getcwd()

    print(path)
	#print("bla")
	#print(request.files)
    try:
     image = request.files["file"]
		#img = cv2.resize(image, (150,150))
    except:
     return "Please upload some image",400

    print(image)
	#print(img)
    target = "D:\\"

    # create image directory if not found
   

    # retrieve file from html file-picker
    
    upload = request.files.getlist("file")[0]

    print("File name: {}".format(upload.filename))
    filename = upload.filename

    # file support verification
    ext = os.path.splitext(filename)[1]
    if (ext == ".jpg") or (ext == ".jpg") or (ext == ".jpg"):
        print("File accepted")
    else:
        return "Please upload another file as only JPG is accepted",400
        return render_template("D:\\anvitha\\error.html", message="The selected file is not supported"), 400

    # save file
    destination = "/".join([target, filename])
    print("File saved to to:", destination)
    upload.save(destination)
    path='D:\\'+filename
    print(path)
	#path = os.path.join('D:',img)
    img = cv2.imread(path,cv2.IMREAD_COLOR)
    img = cv2.resize(img, (150,150))
    print(img)
    X.append(np.array(img))
    X=np.array(X)
    X=X/255
    print(X)
    print(len(X[0]))
    os.chdir('D:')
    print(os.getcwd())
    '''json_file = open("D:\\model1.json", 'r')

    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("D:\\model1.h5")
    print("Loaded model from disk")
    # forward to processing page'''
    print("here")
    pred=loaded_model.predict(X)
    print("heree")
    pred_digits=np.argmax(pred,axis=1)
    print("hereee")
    print(pred_digits[0])
    #lol=dict()
    #lol["answer"]=pred_digits[0]
    return str(pred_digits[0]),200

    #return render_template("processing.html")
	

    return "postt"
@app.route("/app",methods=["GET"])
def helloWorld():
  return "Hello, cross-origin-world!"
app.debug = True
app.run(host='0.0.0.0',port=2166)