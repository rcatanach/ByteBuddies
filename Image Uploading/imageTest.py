# https://www.tutorialspoint.com/how-to-compress-images-using-python-and-pil
# 9 September 2023 -- Compresses an image and then converts it to binary. Also converts from binary to an image.
# 4 October 2023 -- Binary conversion put on the backburner, focusing on uploading and compressing. 
# October 5 2023 -- Added bg removal

# import statements
from PIL import Image
import os 
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import numpy 
from rembg import remove
app = Flask(__name__)

# Keep track of upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create the "binaries" directory if it doesn't exist
BINARIES_FOLDER = 'binaries'
#os.makedirs(BINARIES_FOLDER, exist_ok=True)

# Make sure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Checks for allowed file extensions
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Corrected to match the HTML form
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Removes the background of the image
# Parameters: n -- file name
def removeBackground(n):
    #i = Image.open(n)
    new_n = compress(n)
    i = Image.open(new_n)
    out = remove(i)
    nsplit = n.split('.')
    n = nsplit[-2] + '_bg_rem.png'
    out.save(n)
    os.remove(new_n) # Remove the compressed version, only leaving the one with no bg
    return n

# Compresses images to half size, while optimizing
# PRE: Called by uploadImage
# Parameters: Image file name
def compress(n):

    # Use PILLOW to open images
    i = Image.open(n)

    # Cut in half, add a filter to make it look cleaner
    i = i.resize((int(i.width/2),int(i.height/2)),Image.LANCZOS)

    # Get the directory and filename
    directory, filename = os.path.split(n)

    # Rename 
    new_n = os.path.join(directory, filename.rsplit('.', 1)[0] + '_comp.' + filename.rsplit('.', 1)[1])

    # Save optimized, 85% quality version
    i.save(new_n, optimize=True, quality=85)
    
    # Remove old file, keeping the compressed one
    os.remove(n)
    
    # Print the optimized size
    # i = Image.open(new_n) # Testing
    # print(i.size) # Testing
    return new_n # Returns the new file name

'''
# Converts to binary to be able to store in database
# PRE: Called by uploadImage
# Parameters: Image file name
def convertToBinary(n):
    with open(n, 'rb') as file:
        binaryData = file.read()
    return binaryData
'''

'''
# Uploads image
# Parameters: n -- file name to upload
def uploadImageOld(n):
    compressed_filename = compress(n)
    binary_data = convertToBinary(compressed_filename)
    return binary_data
'''

def uploadImage(n):
    new_n = removeBackground(n)
    return new_n


# Get the main colors from the photo
def getColors(name, num):
    img = Image.open(name)
    return img.getcolors(num)


# Currently doesn't work, trying to write from binary to image
'''
def openBin(n):
    w, h = 50, 100
    with open(n, mode='rb') as f:
        d = numpy.fromfile(f, dtype=numpy.uint8,count=w*h).reshape(h,w)
    PILimage = Image.fromarray(d, 'RGB')
    binarr = numpy.where(PILimage>128, 255, 0)

# Write binary data to a new file
# Parameters: Data -- binary data, n -- new file name
def writeToImage(data, n):
    with open(n, 'wb') as file:
        file.write(data)
'''

# Puts the correct template up
@app.route('/')
def index():
    return render_template('uploadTest.html')
    
# Uploads the photo from HTML
@app.route('/upload', methods=['POST'])
def upload_file():
    #print('upload call') # Testing
    if 'file' not in request.files:
        return redirect(request.url)
    
    file = request.files['file']

    # If there is no file
    if file.filename == '':
        return redirect(request.url)

    # Upload file
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(full_path)
        new_n = compress(full_path) #uploadImage(full_path) # Doesn't remove background anymore
        im = Image.open(new_n)
        
        # Trying to get main colors from picture
        #print(new_n)
        #img = Image.open(new_n)
        #img.convert("RGB")
        #img.show()
        #print(img.getcolors(img.size[0]*img.size[1]))

        # Below code is currently commented out because I am not working on binary uploading. Currently focusing on uploading and compressing. 4 October 2023
        #binary_data = uploadImageOld(full_path)
        #binary_filename = filename.replace('.jpg', '.bin')
        #binary_full_path = os.path.join(BINARIES_FOLDER, binary_filename)
        #writeToImage(binary_data, binary_full_path)
        #openBin(binary_full_path)
        #print(new_n)
        
        return 'Upload success'
    else:
        return 'Invalid file format'

# Runs the file
if __name__ == '__main__':
    app.run(debug=True)

# Testing
#uploadImage('test.jpg')
# writeFile(convertToBinary('testImage.jpg'), 'output.jpg')


